# Workshop Description

There are two steps to this OSM data analysis workshop: 

1. First, we use [Amazon Athena](aws.amazon.com/athena) to query pre-processed OSM historical data.
	- OSM historical editing data is currently available for `Nepal`, `Southeastern Asia`, `Subsaharan Africa`, and `Central America`
	- All OSM `changesets` metadata is available
	- The pre-processed data exists as individual OSM objects with WKT geometries _(not nodes/ways/relations)_
	- The results of these queries are automatically saved to an Amazon S3 bucket.
2. Second, we use [Jupyter Notebooks](http://workshop.yetilabs.science) for an interactive analysis environment to download the query results from S3 and analyze/visualize.

## Getting Started

#### Part 1: Amazon Athena

1. Visit [aws.amazon.com/athena](https://us-east-2.console.aws.amazon.com/athena/home?force&region=us-east-2#query). You'll need to log in with the following credentials: 

		TODO
	
	Once logged in, double check that the region is set to `us-east-2` (Ohio) because that is where the pre-processed OSM data lives. Additionally, you want to make sure that your workgroup is set to `hot-aws-workshop`. 
	
	![Screenshot of Athena](assets/athena-screenshot.png)

	**If there are no tables, see the [Athena Setup](https://github.com/jenningsanderson/aws-hot-workshop/blob/master/setup.md#athena-setup) instructions to load the tables.**		

2. Now you can begin querying the OSM data, see the [Data section](#Data) below for a more detailed description of what is attributes are available. Here are few queries to get you started and familiar with the interface. 

	_Copy the exact queries here and paste them into the query window_.

	1. Count the number of users to ever work on a HOT task:

		```sql 
		SELECT count(DISTINCT(uid))
		FROM changesets
		WHERE lower(changesets.tags['comment']) LIKE '%hotosm%'
		```
		It should return ~ 140,930. That's a lot of people. What about just this year? 
		
		```sql
		SELECT count(distinct(uid))
		FROM changesets
		WHERE lower(changesets.tags['comment']) LIKE '%hotosm%'
			AND changesets.created_at > date '2019-01-01'
		```
		This should return ~ 25,988. Wow, 25k mappers working on at least 1 hot task in 2019. What about users who have more than 1 HOT-related changeset? 
		
		```sql
		SELECT count(uid) FROM (
		  SELECT uid, count(id) AS num_changesets
		  FROM changesets
		  WHERE lower(changesets.tags['comment']) LIKE '%hotosm%'
		  GROUP BY uid
		) WHERE num_changesets > 1
		```
		
		~ 121,860, implying only 20k users only made 1 changeset.
		
		These are simple results in which Athena is only returning single values. Let's dig into the data a bit more...
       
       
	2. Find all HOT-related changesets, grouped by user with basic per-user statistics.
	   
	   ```sql
		SELECT
		    changesets.user,
		    min(created_at) AS first_edit, 
		    max(created_at) AS last_edit, 
		    date_diff('day', min(created_at), max(created_at)) AS lifespan,
		    sum(num_changes) AS total_edits
		FROM 
		    changesets
		WHERE
		    changesets.tags['comment'] LIKE '%hotosm%' -- hotosm changesets only
		GROUP BY 
		    changesets.user 
		ORDER BY lifespan DESC
		```
		
		The results from this query will be a CSV with ~ 140k rows, one per mapper: 
		
		![](assets/lifespan-example.png)
		
		At the upper-right, there is a link to download the results as a CSV file. To explore these results in more depth, we will load these CSV files into a **Jupyter Notebook**, as described next. For now, `right-click` this link and copy the link address: 
		
		![](assets/save-as.png)
				
		You may want to paste this link somewhere safe to hold onto it, it should look similar to this: _https://us-east-2.console.aws.amazon.com/athena/query/results/23f6baab-b1c7-40b5-902c-42901f2447df/csv_

#### Part 2: Logging into the Jupyter Notebooks

1. There is an instance of JupyterHub running on an Amazon EC2 machine located at [workshop.yetilabs.science:8000](http://workshop.yetilabs.science:8000) that will allow each workshop participant to run their own analysis environment.
2. **Tell the workshop organizers what username you would like to use**.
	
		TODO: This might be different, perhaps pre-made accounts like workshop-1, workshop-2... 
		For testing, all of the planets exist:
		
		username: mars
		password: mars
		
	Or `saturn | saturn`, `venus | venus`, `pluto | pluto`, `neptune | neptune`...
	
4. When you are successfully logged in and the notebook server is running, you should see a page that looks like this: 

	![Jupyter Notebook Home](assets/home.png) 

5. Click on a notebook to launch.


#### Part 3: Other Notebooks
There are `X` notebooks with sample code that describes the queries used to generate  


#### Resources 

1. For spatially bounded queries, [this bounding box tool](https://boundingbox.klokantech.com/) can quickly construct WKT bounding boxes. I recommend having this tool open in another tab for quick reference.


<hr>
<br>
## Data

Our dataset has gone through one step of pre-processing. Using the [OSMesa utility](https://github.com/azavea/osmesa), the raw node/way/relation elements have been converted into single OSM objects with WKT geometries. This conversion also accounts for _minor versions_, the unaccounted versions of ways and relations created by modifying the child object (like squaring a building or fixing a road).

Therefore the data looks slightly different from the original OSM data model, namely the following fields: 

|Attribute (Column) | Description|
|-----|-----|
| `updated` | When this version/minor version of the object was created |
| `valid_until` | When this particular vernor version was altered, making this version of the object no longer the most recent |
| `minor_version` | How many times the geometry / child elements of the primary element has been modified | 
| `version` | The version of this object that corresponds to the version of the OSM element ||
| `geom` | The geometry of this version of the object (WKT) |

<br>
<br>
<hr>
