#!/usr/bin/env python
import sys
import argparse
import gitlab
import snyk

#
# Serach for projects in gitlab based on the given name list(with namespace) 
#
def get_gitlab_projects(gl, project_list):
    projects = []
    for project_name_with_namespace in project_list:
        try:
            projects.append(gl.projects.get(project_name_with_namespace))
        except:
            print(project_name_with_namespace + " project not found in gitlab")
    return projects

#
# Check if the snyk web hook is present in the given project
#
def is_snyk_hook_present(gitlab_project, broker_url):
    hook_found = False
    for hook in gitlab_project.hooks.list():
        if broker_url in hook.url:
            hook_found = True
            break
    return hook_found

#
# Take the given project list (names with namespaces), and check in each of them if the snyk hook is present
#
def checkForSnykWebhook(gl, broker_url, project_list):
    gitlab_projects = get_gitlab_projects(gl,project_list)
    projects_with_webhook = []
    projects_witout_webhook = []
    for gitlab_project in gitlab_projects:
        if is_snyk_hook_present(gitlab_project, broker_url):
            projects_with_webhook.append(gitlab_project.path_with_namespace)
        else:
            projects_witout_webhook.append(gitlab_project.path_with_namespace)
    
    return projects_with_webhook, projects_witout_webhook

#
# Argument parsing for CLI usage
#
def parse_args():
    parser = argparse.ArgumentParser("snyk_gitlab_map")
    parser.add_argument("-u","--gitlab_url", required=True, help="Gitlab URL", type=str)
    parser.add_argument("-gt","--gitlab_token", required=True, help="Gitlab API token", type=str)
    parser.add_argument("-st","--snyk_token", required=False, help="Snyk API token", type=str)
    parser.add_argument("-b","--broker_url", required=True, help="Snyk broker URL", type=str)

    parser.add_argument("-org","--snyk_org", required=('-st' in sys.argv) or ('--snyk_token' in sys.argv), help="Snyk organisation ID. If given, will check for the snyk webhook presence in gitlab for all of the projects in the org", type=str)
    parser.add_argument("-l","--project_list", required=not (('-st' in sys.argv) or ('--snyk_token' in sys.argv)), help="List of projects to check for the snyk webhook, comma separated", type=str)
    return parser.parse_args()

#
# Main
#
def main():
    args = parse_args()

    gl = gitlab.Gitlab(url=args.gitlab_url, private_token=args.gitlab_token)

    projects_list = []

    if args.project_list:
        print("Searching for snyk webhook in gitlab for the given project list.")
        projects_list = args.project_list.split(',')
        
    else:
        print("Searching for snyk webhook in gitlab for the given snyk org.")
        sk = snyk.SnykClient(args.snyk_token)
        projects_list = []
        for snyk_project in sk.organizations.get(args.snyk_org).projects.all():
            if (snyk_project.origin == 'gitlab') and hasattr(snyk_project, 'remoteRepoUrl'):
                project_name = snyk_project.remoteRepoUrl.split('.com/')[-1]
                if not project_name in projects_list:
                    projects_list.append(project_name)

    projects_with_webhook,projects_witout_webhook = checkForSnykWebhook(gl, args.broker_url, projects_list)

    print("Projects with snyk webhook:")
    print(projects_with_webhook)
    print("Projects without snyk webhook:")
    print(projects_witout_webhook)

if __name__ == "__main__":
    main()