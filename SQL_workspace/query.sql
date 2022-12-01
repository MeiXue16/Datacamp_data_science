# 查询2019 年 7 月的跑步分钟数
SELECT 
	SUM(duration_mins) 
FROM 
	runs_fact as r
INNER JOIN week_dim as w ON r.week_id = w.week_id
WHERE w.month = 'July' and w.year = '2019';