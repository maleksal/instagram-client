from client.InstaC import InstaClient

# Authenticate using credentials
client = InstaClient('username', 'password')

# Get user profile
profile = client.get_username_profile('profile_username')

# Get user first 24 followings
followings = profile.followings()
print(followings)


# Get all followings
while followings['data']["user"]["edge_follow"]["page_info"]["has_next_page"]:
    print()
    end_cur = followings['data']['user']["edge_follow"]["page_info"]["end_cursor"]
    followings = profile.followings(end_cursor=end_cur)
    print(followings)
