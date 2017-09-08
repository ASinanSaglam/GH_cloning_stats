import requests, sys, pickle, datetime, argparse, getpass, os

# Get user arguments, in particular user/password 
parser = argparse.ArgumentParser("A simple script to gather and store cloning/release data off of GitHub")
parser.add_argument('-gu', '--ghusr', type=str,
                     help="GitHub user account for the repo that's in question")
parser.add_argument('-gr', '--ghrep', type=str,
                     help="GitHub user repo for the repo that's in question")
parser.add_argument('-pu', '--puser', type=str, default=None,
                     help="GitHub account name with push access to the repo, for cloning data")
parser.add_argument('-pt', '--ptoken', action='store_true', default=False,
                     help="Use GitHub token instead of a password. An environment variable called \
                           GH_CLONE_TOKEN is needed with the correct token in place.")
parser.add_argument('-pp', '--ppswd', type=str, default=None,
                     help="GitHub account password with push access to the repo, for cloning data \
                           you can omit this and the program will interactively ask for your password \
                           if you have specified a GitHub push access user with -pu or --puser")
parser.add_argument('-o', '--output', type=str, default="ghstats.pickle",
                     help="Output file name, if the script is used before, use the same file name \
                           if you want to avoid creating a new file, it'll be updated. Everything \
                           is saved as a python pickle file and the default name of the file is   \
                           (ghstats.pickle)")
args = parser.parse_args()
gh_usr = args.ghusr
gh_rep = args.ghrep
user = args.puser
pswd = args.ppswd
ptoken = args.ptoken
if ptoken:
    # Get os environment var and cry if it's not available
    print("Acquiring token")
    try:
        token = os.environ["GH_CLONE_TOKEN"]
    except:
        print("Cannot find environment variable 'GH_CLONE_TOKEN'")

output = args.output
newFile = False
try:
    outfile = open(args.output, 'r+')
except IOError:
    outfile = open(args.output, 'w')
    newFile = True

# Get user/pass, eventually security stuff here
# NOT IMPLEMENTED YET

# Now request the stats for cloning and releases
base_url = "https://api.github.com/repos"
repo_url = base_url + "/" + gh_usr + "/" + gh_rep + "/"

# IF push access is avilable, update cloning stats
print("Attempting to acquire cloning data")
if user and (pswd or ptoken):
    passwrd = pswd or token
    clone_stats_req = requests.get(repo_url + "traffic/clones", auth=(user, passwrd))
    clonej = clone_stats_req.json()
elif user and not pswd:
    print("Please enter GitHub account password for %s"%user)
    pswd = getpass.getpass()
    clone_stats_req = requests.get(repo_url + "traffic/clones", auth=(user, pswd))
    clonej = clone_stats_req.json()
else:
    clonej = None

# let's just pull latest release at the moment
print("Acquiring release data")
release_stats_req = requests.get(repo_url + "releases/latest")
releasej = release_stats_req.json()

# get the current date
date_str = datetime.datetime.now().date().isoformat()

print("Saving")
if newFile:
    print("New file")
    # If new, just make a new file
    releasej["data_updated"] = date_str
    stats_dict = {"release_data": {'latest': releasej}, "cloning_data": {date_str: clonej}}
    outfile.close()
    outfile = open(args.output, 'w')
    pickle.dump(stats_dict, outfile)
else:
    print("Updating file")
    # If loading, we update the cloning data directly 
    stats_dict = pickle.load(outfile)
    stats_dict["cloning_data"][date_str] = clonej
    # and check for a new release 
    rel_id = stats_dict["release_data"]["latest"]["id"]
    if releasej["id"] == rel_id:
        # if the same release if, update the assets section
        stats_dict["release_data"]["latest"]["assets"] = releasej["assets"]
        stats_dict["release_data"]["latest"]["data_updated"] = date_str
    else:
        # if not the same, move old latest to id and move the new release to latest
        cur_id = stats_dict["release_data"]["latest"]["id"]
        stats_dict["release_data"][cur_id] = stats_dict["release_data"]["latest"]
        releasej["data_updated"] = date_str
        stats_dict["release_data"]["latest"] = releasej
    outfile.close()
    outfile = open(args.output, 'w')
    pickle.dump(stats_dict, outfile)


