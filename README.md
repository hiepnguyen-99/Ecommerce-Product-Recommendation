## Introduction
This project has been built a chatbot for E-commerce (EcommerceBot) to support customers and enhance experience

## Dataset
Amazon question/answer data by Julian McAuley
https://cseweb.ucsd.edu/~jmcauley/datasets/amazon/qa/

## Features

- **HTML** - Frontend
- **Python** - Backend: build a RAG structual

    - **Retriever**: used sentence-transformers/all-MiniLM-L6-v2 pretrained model to tokenize and embedding data, then find the related documents

    - **Generator**: used SRDdev/QABERT-small with input is question + context, output is answer

## Project Structure

```
Ecommerce-QA/
├── assets/             # Images
├── data/          
├── model/              # RAG
├── pages/              # Include index.html 
└── app.py             
```

## User Guide

1. Clone repository to local
2. Install the required libraries:
```bash
pip install -r requirements.txt
```
3. Run 
```bash
app.py
```
4. Access host: http://127.0.0.1:5500/pages/ChatInterface.html