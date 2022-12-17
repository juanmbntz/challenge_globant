CREATE TABLE human_resources.hirings_by_department as (
WITH tmp as (

SELECT 
    dep.id                                                as id
  ,dep.department                                         as department
  ,job.job                                                as job

FROM human_resources.hired_employees emp

LEFT JOIN human_resources.departments dep 
on dep.id = emp.department_id 
LEFT JOIN human_resources.jobs job 
on job.id = emp.job_id

-- only employees hired in 2021
WHERE extract(year from date(emp.datetime)) = 2021

)

-- CTE with average hirings by department
, avg_hirings as (
  select 
    -- how many times a department appears in hired employees table (number of hirings) divided by number of departments
    count(department)/count(distinct(department)) as avg_dep_hirings
  from tmp
)

SELECT 
   tmp.id                         as id
  ,tmp.department                 as department
  ,count(department)              as hired

FROM tmp 
GROUP BY tmp.id, tmp.department
-- only departments that hired above the average
HAVING count(department) > (select avg_dep_hirings from avg_hirings)
ORDER BY hired DESC, id ASC
)
;

