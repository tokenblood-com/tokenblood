# tokenblood 

## Description

TBA.

## Dataset location

Source dataset is stored on `/data` directory on google vm and have following structure. 

When adding a new dataset please use following structure: `<task_name>/<dataset_name>/<version_name/eval.csv> and not forget to add README.md to directory.

```text
data/
└── personal_info_extraction
    └── ai4privacy
        ├── v0
        │   ├── README.md
        │   └── eval.csv
        └── v1
            ├── README.md
            ├── cleaned.md
            ├── eval.csv
            └── raw.md
```
- To upload dataset to google cloud vm, use following command: `rsync -avz data machine:/data`.
- To upload dataset for local development, use following command: `rsync -avz machine:/data data`.

## Useful commands

- build backend docker: `docker build -t tokenblood-com/backend -f Dockerfile .`
- run backend docker: `docker run -p 8000:8000 --env-file .env tokenblood-com/backend`
