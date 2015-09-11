""" Bootstraps instance of Docker container for PRISONER demonstration.
Requests Facebook app ID and secret, shows url for demo app
"""
import platform

root_path = "/usr/bin/prisoner-demo/" # docker
#root_path = "" # local



if __name__ == "__main__":
    print "PRISONER Demonstration"
    print "======================"

    print "Before running this experiment, please register an app with the Facebook Developers dashboard <https://developers.facebook.com/apps/>."

    print "Provide localhost as the Site URL and app domain on your app's settings page."

    print "For more information about getting started, see the documentation for this demo at http://prisoner.cs.st-andrews.ac.uk/docs/<TODO>."

    print "\n Enter the App ID for your Facebook app:"
    app_id = raw_input()

    print "Enter the App Secret for your Facebook app:"
    app_secret = raw_input()

    print "\n Enter the API key for your Twitter app:"
    twitter_key = raw_input()

    print "Enter the App Secret for your Twitter app:"
    twitter_secret = raw_input()

    replacements = {'$APP_ID':app_id, "$APP_SECRET":app_secret,
    "$TWITTER_KEY":twitter_key, "$TWITTER_SECRET": twitter_secret}
    lines = []
    with open('%sstatic/policy/design_src.xml' % root_path) as infile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            lines.append(line)
    with open('%sstatic/policy/design.xml' % root_path, "w") as outfile:
        for line in lines:
            outfile.write(line)

    print "Policy updated. Now starting PRISONER..."
