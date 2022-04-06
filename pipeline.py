# from transformers import pipeline

import pandas as pd
import numpy as np
import json

import torch
# from keras.preprocessing.sequence import pad_sequences

from transformers import BertTokenizer
from transformers import BertForTokenClassification
from utils import *

class PyTorchBackend:
    def __init__(self):
    
        self.tag2idx = {'B-art': 0,
        'B-eve': 1,
        'B-geo': 2,
        'B-gpe': 3,
        'B-nat': 4,
        'B-org': 5,
        'B-per': 6,
        'B-tim': 7,
        'I-art': 8,
        'I-eve': 9,
        'I-geo': 10,
        'I-gpe': 11,
        'I-nat': 12,
        'I-org': 13,
        'I-per': 14,
        'I-tim': 15,
        'O': 16}

        self.idx2tag = {}
        for key in list(self.tag2idx.keys()) :
            self.idx2tag[self.tag2idx[key]] = key

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
        self.model     = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=len(self.tag2idx))
        self.model.load_state_dict(torch.load("ner.dataset.4.pth",map_location=torch.device('cpu')))
        self.model.eval()

        # self.classifier = pipeline("sentiment-analysis")

    def __call__(self, request):

        # return json.loads(request.data) #request.data #"AAAAAAA"

        MAX_LEN = 75
        bs      = 32
        device  = 'cpu'

        # if not request.json :
        #     abort(400, 'Did not receive any content in POST request!')

        # Check that we have all requisite fields.
        # sent_json = request.json.copy()

        # if 'tokens' not in sent_json.keys() or 'rects' not in sent_json.keys() :
        #     abort(400, 'Did not receive sentence data in POST request!')

        # print(sent_json)

        # words = sent_json['tokens']
        # rects = sent_json['rects']

        sent_json = json.loads(request.data)
        words     = [t['token'] for t in sent_json]
        rects     = [t['id'] for t in sent_json]

        assert len(words)==len(rects)

        tt,tr = format_token_arr(self.tokenizer,words,rects)
        tttag = tag_sentences(self.tokenizer,self.model,self.idx2tag,tt)

        ttago = []
        tro   = []
        for i in range(len(tttag)) :
            assert len(tttag[i])==len(tr[i])
            ttago.extend(tttag[i])
            tro.extend(tr[i])

        ttagf,trf = filter_partial_tags(ttago,tro)

        # for i in range(len(ttagf)) : 
        #     print(len(ttagf[i]),len(trf[i]))
        #     assert len(ttagf[i]) == len(trf[i])

        jout = [{'token':ttagf[i]['token'],'id':trf[i],'label':ttagf[i]['label']} for i in range(len(ttagf))]

        #ttag_comb,tr_comb = combine_tags(ttagf,trf)

        # for i in range(len(ttag_comb)) : 
        #     print(len(ttag_comb[i]),len(tr_comb[i]))
        #     assert len(ttag_comb[i]) == len(tr_comb[i])

        return json.dumps(jout)

        # return jsonify( { 'result': {'tokens' : ttag_comb, 'rects' : tr_comb}} )

        # [result] = self.classifier(str(request.data))
        # return result["label"]

import ray
from ray import serve

ray.init(address="auto", ignore_reinit_error=True)
serve.init()

serve.create_backend("pytorch_backend", PyTorchBackend)
serve.create_endpoint("sentiment_endpoint", backend="pytorch_backend", route="/sentiment")
serve.set_traffic("sentiment_endpoint", {"pytorch_backend": 1.0})
