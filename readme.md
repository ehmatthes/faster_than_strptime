What's faster than strptime()?
---

I was working on a project recently where the code was spending 2.5 seconds in calls to `datetime.strptime()`. I started wondering if I could do anything to speed this up, and tried a number of different approaches. The code in this repository makes it easy to compare a variety of approaches to converting a string-based timestamp into a datetime object. I wrote [an article](http://ehmatthes.com/blog/faster_than_strptime/) about these different approaches.

## Running this code:

- Clone and create a virtual environment:
    - `$ git clone https://github.com/ehmatthes/faster_than_strptime.git`
    - `$ cd faster_than_strptime`
    - `faster_than_strptime$ python3 -m venv venv`
    - `faster_than_strptime$ source venv/bin/activate`
    - `faster_than_strptime$ pip install -r requirements.txt`
- Generate some data:
    - `faster_than_strptime$ python generate_data.py 500_000`
- Process the data using one of the approaches:
    - `faster_than_strptime$ python process_data.py fromisoformat`
