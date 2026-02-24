# Datasheet for Dataset: [Dataset Name]

## Motivation
*   **For what purpose was the dataset created?** [e.g., To train a sentiment analysis model for financial news.]
*   **Who created the dataset?** [e.g., Team X, Company Y, or Individual Z.]
*   **Who funded the creation of the dataset?** [e.g., Grant A, Department B.]

## Composition
*   **What do the instances that comprise the dataset represent?** [e.g., News articles, images of plants, audio recordings.]
*   **How many instances are there in total?** [e.g., 10,000 articles.]
*   **Does the dataset contain all possible instances or is it a sample?** [e.g., Sample of articles from 2020-2025.]
*   **What data does each instance consist of?** [e.g., Text, metadata, labels.]
*   **Is there a label or target associated with each instance?** [e.g., Sentiment score (0-1).]
*   **Is any information missing from individual instances?** [e.g., Some articles missing author metadata.]
*   **Are there recommended data splits?** [e.g., Train/Val/Test split provided.]
*   **Are there any errors, sources of noise, or redundancies in the dataset?** [e.g., Duplicate articles removed.]
*   **Is the dataset self-contained, or does it link to or rely on external resources?** [e.g., Self-contained JSONL file.]
*   **Does the dataset contain data that might be considered confidential?** [e.g., No PII included.]
*   **Does the dataset contain data that might be offensive, insulting, or threatening?** [e.g., Filtered for hate speech.]
*   **Does the dataset relate to people?** [e.g., No, financial news only.]
*   **Does the dataset identify any subpopulations?** [e.g., No.]
*   **Is it possible to identify individuals, either directly or indirectly, from the dataset?** [e.g., No.]
*   **Does the dataset contain data that might be considered sensitive in any way?** [e.g., No.]

## Collection Process
*   **How was the data associated with each instance acquired?** [e.g., Web scraping via Scrapy.]
*   **What mechanisms or procedures were used to collect the data?** [e.g., API, manual entry, sensors.]
*   **If the dataset is a sample from a larger set, what was the sampling strategy?** [e.g., Random sampling.]
*   **Who was involved in the data collection process?** [e.g., Data Engineers.]
*   **Over what timeframe was the data collected?** [e.g., Jan 2025 - Dec 2025.]
*   **Were any ethical review processes conducted?** [e.g., Internal ethics review passed.]

## Preprocessing/Cleaning/Labeling
*   **Was any preprocessing/cleaning/labeling of the data done?** [e.g., Tokenization, lowercasing, removal of stop words.]
*   **Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data?** [e.g., Yes, in `data/raw/`.]
*   **Is the software used to preprocess/clean/label the instance available?** [e.g., Yes, in `src/data/`.]

## Uses
*   **Has the dataset been used for any tasks already?** [e.g., Yes, trained baseline model.]
*   **Is there a repository that links to or uses the dataset?** [e.g., GitHub repo link.]
*   **What (other) tasks could the dataset be used for?** [e.g., Topic modeling, entity recognition.]
*   **Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?** [e.g., Bias towards US markets.]
*   **Are there tasks for which the dataset should not be used?** [e.g., Predicting individual credit scores.]

## Distribution
*   **Will the dataset be distributed to third parties outside of the entity on behalf of which the dataset was created?** [e.g., No, internal use only.]
*   **How will the dataset will be distributed?** [e.g., S3 bucket access.]
*   **When will the dataset be distributed?** [e.g., Immediately.]
*   **Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?** [e.g., Proprietary license.]
*   **Have any third parties imposed IP-based or other restrictions on the data associated with the instances?** [e.g., No.]
*   **Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?** [e.g., No.]

## Maintenance
*   **Who is supporting/hosting/maintaining the dataset?** [e.g., Data Engineering Team.]
*   **How can the owner/curator/manager of the dataset be contacted?** [e.g., Email/Slack.]
*   **Is there an erratum?** [e.g., No.]
*   **Will the dataset be updated?** [e.g., Yes, monthly updates.]
*   **If the dataset relates to people, are there applicable limits on the retention of the data?** [e.g., N/A.]
*   **Will older versions of the dataset continue to be supported/hosted/maintained?** [e.g., Yes, in archive.]
*   **If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?** [e.g., Pull requests welcome.]
