import pickle, argparse

parser = argparse.ArgumentParser("A simple script to print stored cloning/release info")
parser.add_argument('-i', '--input', type=str, default='ghstats.pickle',
                     help="Input python pickle file")
parser.add_argument('-pc', '--print_clone', action='store_false', default=True,
                     help="Stops printing of cloning data")
parser.add_argument('-pr', '--print_release', action='store_false', default=True,
                     help="Stops printing of release data")
args = parser.parse_args()

input_file = args.input
print_clone = args.print_clone
print_release = args.print_release

f = open(args.input, 'r')
st = pickle.load(f)

cln_st = st['cloning_data']
rls_st = st['release_data']

def _print_rls(key, rls):
    print("Release name: %s, "%key + rls['name'])
    print("Info: %s"%rls['body'])
    print("HTML URL: %s"%rls['html_url'])
    print("TARBALL URL: %s"%rls['tarball_url'])
    print("ZIPBALL URL: %s"%rls['zipball_url'])
    _print_assets(rls['assets'])

def _print_assets(assets):
    if len(assets) == 0:
        print("No asset found!")
    else:
        for asset in assets:
            _print_asset(asset)

def _print_asset(asset):
    print("###")
    print("Printing asset info for: %s"%asset['name'])
    print("Created at: %s, updated at: %s"%(asset['created_at'], asset['updated_at']))
    print("Type: %s"%asset['content_type'])
    print("URL: %s"%asset['browser_download_url'])
    print("Download count: %s"%asset['download_count'])
    print("###")

def print_release_info(rls_st):
    rls_keys = rls_st.keys()
    print("#################################")
    print("Printing release info")
    print("#################################")
    try:
        lt_rel = rls_st['latest']
        print("Latest Release")
        _print_rls("Latest", lt_rel)
    except KeyError:
        print("Latest release info not found!")

    for key in rls_keys:
        if key != "latest":
            print("########")
            _print_rls(key, rls_st[key])
    print("#################################")
    print("Done printing release info")
    print("#################################")

def print_clone_info(cln_st):
    dates = sorted(cln_st.keys())
    print("Printing cloning info")
    print("#################################")
    print("Cloning data gathered on the following dates")
    print(", ".join(dates))
    for date in dates:
        ccln = cln_st[date]
        try:
            print("On %s there were %i clones and %i were unique. Total in past 2 weeks was: %s"%(\
                   date,ccln['clones'][0]['count'],ccln['clones'][0]['uniques'],ccln['count']))
        except KeyError:
            pass
    print("#################################")
    print("Done printing cloning info")
    print("#################################")

if print_release:
    print_release_info(rls_st)
if print_clone:
    print_clone_info(cln_st)
