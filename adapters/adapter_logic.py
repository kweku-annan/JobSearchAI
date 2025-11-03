#!/usr/bin/env python
"""
 -- adapter_logic.py --
    Defines logic for which adapter to call and how to concatenate results
"""

from adapters.jobicy import  parse_jobicy_job
from adapters.remoteok import parse_remoteok_job
from adapters.remotive import parse_remotive_job
from adapters.arbeitnow import parse_arbeitnow_job

def aggregate_job_listings():
    """Aggregate job listings from multiple adapters based on API availability"""
    all_jobs = []
    try:
        remotive = parse_remotive_job()
        all_jobs.extend(remotive)
    except Exception as e:
        # print(f"Error fetching from primary adapters: {e}")
        try:
            remoteok = parse_remoteok_job()
            all_jobs.extend(remoteok)
            # jobicy = parse_jobicy_job()
            # all_jobs.extend(jobicy)
        except Exception as e:
            # print(f"Error fetching from JobIcy adapter: {e}")
            try:
                arbeitnow = parse_arbeitnow_job()
                all_jobs.extend(arbeitnow)
            except Exception as e:
                print(f"Error fetching from ArbeitNow adapter: {e}")

    return all_jobs