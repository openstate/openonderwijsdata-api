# Contributing to the Open Onderwijs Data API

Want to get involved with the Open Onderwijs Data API? Here's how you can help!

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

## Using the issue tracker

The [issue tracker](https://github.com/openstate/openonderwijsdata-api/issues) is the preferred channel for submitting bug reports, feature requests and pull requests.

## Bug reports

Spot an error in the way data is formatted? Getting unexpected error when making a call to the API? Than please submit a bug report. Good bug reports are extremely helpful in order to improve the code, and the project in general.

Some guidelines when submitting a bug report:

- Check if the issue hasn't already been reported.
- Be as detailed as possible, people reading the report shouldn't have to chase you up for more information. Describe the problem thoroughly, so others can try to reproduce it.

## Feature requests

Feature requests are welcome, but take a moment to find out whether your idea fits the scope and goals of the project. It's up to you to make a strong case to convince others of the merits of the feature your are requesting. Please provide as much detail and context as possible.

## Pull requests

We really like to receive good pull requests for patches, new features or improvements.

Our advice is to first discuss changes, before you start working on a large pull-request (for instance, when implementing new features or significant refactoring of the code). Otherwise you risk spending time on something that won't be (directly) merged into the project.

Please adhere to the [coding conventions](dev-coding-conventions) used throughout the project.

To submit a pull request, follow this process:

1. [Fork the project](http://help.github.com/fork-a-repo/) and clone your fork::

	```
	   git clone https://github.com/<your-username>/openonderwijsdata-api.git
	   cd openonderwijsdata-api
		   git remote add upstream https://github.com/openstate/openonderwijsdata-api.git
	```

2. Always make sure you are working with a recent version. To get the latest changes from upstream::

	```
	   git checkout master
	   git pull upstream master
	```

3. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix::

	```
	   git checkout -b <topic-branch-name>
	```

4. Push your topic branch up to your fork:

	```
	   git push origin <topic-branch-name>
	```

5. Open a [Pull Request](https://help.github.com/articles/using-pull-requests/) with a clear title and description against the master branch.

# Code formatting

- We currently target Python 2.7 as a minimum version
- Follow the style you see used in the primary repository! Consistency with the rest of the project always trumps other considerations.
- We try to use the [PEP 8](http://legacy.python.org/dev/peps/pep-0008/) styleguide for all Python code. 
