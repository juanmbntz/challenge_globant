CREATE TABLE human_resources.hirings_by_quarter as (
WITH tmp as (
SELECT 
   dep.department                                         as department
  ,job.job                                                as job
  ,date(emp.datetime)                                     as date_time
  ,CASE
    WHEN date(emp.datetime) <= '2021-03-31' THEN  'Q1'
    WHEN date(emp.datetime) <= '2021-06-30' THEN  'Q2'
    WHEN date(emp.datetime) <= '2021-09-30' THEN  'Q3'
    ELSE                                          'Q4'
  END                                                     as quarter
FROM human_resources.hired_employees emp
LEFT JOIN human_resources.departments dep 
on dep.id = emp.department_id 
LEFT JOIN human_resources.jobs job 
on job.id = emp.job_id

-- only employees hired in 2021
WHERE extract(year from date(emp.datetime)) = 2021
)

SELECT

  tmp.department 
  ,tmp.job 
  ,sum( if((tmp.quarter = 'Q1'),1,0)) as Q1 -- count row if quarter is q1
  ,sum( if((tmp.quarter = 'Q2'),1,0)) as Q2 -- count row if quarter is q2
  ,sum( if((tmp.quarter = 'Q3'),1,0)) as Q3 -- count row if quarter is q3
  ,sum( if((tmp.quarter = 'Q4'),1,0)) as Q4 -- count row if quarter is q4

FROM tmp
GROUP BY 
department, job
ORDER BY 
department ASC, job ASC
)
;
