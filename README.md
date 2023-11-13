# Snyk Helpers

This repo contains a collection of tools to improve/complement Snyk usage.

The toolkit currently contains:
1. snyk_gitlab_ci_map.py - Enumerate the presence of snyk step in gitlab CI/CD pipelines


### 1. snyk_gitlab_ci_map
This tool relies on gitlab and snyk apis to check for the presence of the snyk webhook in Gitlab projects.
This allows to know if snyk checks are integrated in the CI/CD pipelines.
It can be used by providing a comma separated list of project (name with namespace), or by providing the snyk org.


1. Usage with a comma separated list of project 
```
python3 snyk_gitlab_ci_map.py --gitlab_url https://my.hosted.gitlab.mycompany.com --gitlab_token XXX --broker_url https://my.hosted.snyk-broker.mycompany.com --project_list namespace1/gitlab-project1,namespace2/gitlab-project2

# Output
Searching for snyk webhook in gitlab for the given project list.
Projects with snyk webhook:
['namespace1/gitlab-project1','namespace2/gitlab-project2']
Projects without snyk webhook:
[]
```

2. Usage with Snyk org
```
python3 snyk_gitlab_ci_map.py --gitlab_url https://my.hosted.gitlab.mycompany.com --gitlab_token XXX --snyk_token XXX --broker_url https://my.hosted.snyk-broker.mycompany.com --snyk_org XXX

# Output
Searching for snyk webhook in gitlab for the given snyk org.
Projects with snyk webhook:
['namespace1/gitlab-project1','namespace2/gitlab-project2']
Projects without snyk webhook:
[]
```
