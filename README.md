#Bahamas Scrapper

#####Site URL
        http://laws.bahamas.gov.bs/
#####Required
    - Python: 2.7.14
    - Mysql Server
    - Database credentials providing in constants.py file

#####Steps for Running Scrapper
    - RUN pip install -r requirements (for installing required scrapper packages)
    - Scrapper Jobs:
        - 1: Populate the Principal and Amending Acts Passed for all Years
        - 2: Populate the Subsidiary Legislation Table
        - 3: Build law relations for the alphabetical list of the laws
        - 4: Update repeal acts status and repeal dates
        
    - Command pattern to run a job:
        - python main.py --job job_number
        - e.g. python main.py --job 1 (if you want to run job 1)
        