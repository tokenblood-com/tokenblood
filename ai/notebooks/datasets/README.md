# Open source datasets

- [AI4Privacy](https://huggingface.co/datasets/ai4privacy/open-pii-masking-500k-ai4privacy)
- [Isotonic](https://huggingface.co/datasets/Isotonic/pii-masking-200k)


## AI4Privacy 

### Link to notebook: [ai4privacy.ipynb](./ai4privacy.ipynb)

- multi-language dataset, containing 120k/30k train/val samples in English

- contains tokens GIVENNAME_ (containing first name and middle name), SURNAME_ (containing last or family name)

- have 13k/3k train/val examples containing givenname/surname from multiple people

- manually checked 100 examples from train split and didn't find any errors in labelling


## Isotonic

### Link to notebook: [isotonic.ipynb](./isotonic.ipynb)

- multi-language dataset, containing 17k train samples in English

- contains tokens FIRSTNAME_ (containing first name), MIDDLENAME_ (containing middle name), LASTNAME_ (containing last or family name)

- have 457 train/val examples containing names from multiple people

- manually checked 100 examples from train split, find lots of errors in labelling MIDDLENAME_ tokens, think it's not useful for webarena