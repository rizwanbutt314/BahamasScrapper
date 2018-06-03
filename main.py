import task_acts_by_year
import task_subsidiary_by_year
import task_build_law_relations
import task_update_repeal_acts
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Bahamas Parser CommandLine Help')
    parser.add_argument('--job', help='Job number to run')
    args = parser.parse_args()

    return args


def jobs_description(job_number):
    jd = {
        '1': 'Populate the Principal and Amending Acts Passed for all Years',
        '2': 'Populate the Subsidiary Legislation Table',
        '3': 'Build law relations for the alphabetical list of the laws',
        '4': 'Update repeal acts status and repeal dates',
    }
    return jd[job_number]


def main():
    args = parse_arguments()
    JOB_1_URL = "http://laws.bahamas.gov.bs/cms/en/legislation/acts-by-year.html?view=acts_by_year"
    JOB_2_URL = "http://laws.bahamas.gov.bs/cms/en/legislation/subsidiary-by-year.html?view=instruments_by_year"
    JOB_3_URL = "http://laws.bahamas.gov.bs/cms/en/legislation/laws/by-title.html?view=acts_alpha"
    JOB_4_URL = "http://laws.bahamas.gov.bs/cms/en/legislation/repealed.html"

    if args.job is None:
        print("No job number given...!")
    else:
        job_number = str(args.job)
        print("\n")
        print("Running Job# " + job_number)
        print("Description: " + jobs_description(job_number))
        print("\n")
        if job_number == '1':
            task_acts_by_year.main(JOB_1_URL)
        elif job_number == '2':
            task_subsidiary_by_year.main(JOB_2_URL)
        elif job_number == '3':
            task_build_law_relations.main(JOB_3_URL)
        elif job_number == '4':
            task_update_repeal_acts.main(JOB_4_URL)


main()
