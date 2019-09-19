HOT-related changesets per day

```sql
SELECT 
  date_trunc('day', created_at) AS day, 
  SUM(num_changes) AS changes, 
  COUNT(id) AS changesets, 
  COUNT(DISTINCT(uid)) AS users
FROM 
  changesets
WHERE 
  changesets.tags['comment'] LIKE '%hotosm%'
GROUP BY 
  date_trunc('day', created_at)
ORDER BY 
  date_trunc('day', created_at) ASC
```

How about the length of all the highways in Nepal?


```sql
select nepal.tags['highway'], sum(ST_Length(geom))
from nepal
where element_at(nepal.tags, 'highway') IS NOT NULL
GROUP BY nepal.tags['highway']
ORDER BY sum(ST_Length(geom)) DESC
```

Filter for only current version of the map...

```sql
select 
  nepal.tags['highway'], 
  sum(ST_Length(geom))
FROM nepal
WHERE 
  element_at(nepal.tags, 'highway') IS NOT NULL AND 
  nepal.valid_until IS NULL
GROUP BY nepal.tags['highway']
ORDER BY sum(ST_Length(geom)) DESC
```

How bout the total amount of highway that was edited during the earthquake response and has not been updated since?

```sql
select 
  nepal.tags['highway'], 
  sum(ST_Length(geom))
FROM nepal
WHERE 
  element_at(nepal.tags, 'highway') IS NOT NULL AND 
  nepal.valid_until IS NULL
  AND updated > date '2015-4-25' AND updated < date '2015-05-30'
GROUP BY nepal.tags['highway']
ORDER BY sum(ST_Length(geom)) DESC
```

```

SELECT 
  nepal.tags['highway'], 
  count(distinct(changesets.uid)) AS num_users,
  sum(ST_Length(geom))
FROM nepal
JOIN changesets ON changesets.id = nepal.changeset
WHERE 
  element_at(nepal.tags, 'highway') IS NOT NULL AND 
  nepal.valid_until IS NULL
  AND updated > date '2015-4-25' AND updated < date '2015-05-30'
GROUP BY nepal.tags['highway']
ORDER BY sum(ST_Length(geom)) DESC

```