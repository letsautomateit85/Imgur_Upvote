import requests, json, math
from requests.exceptions import HTTPError

username= 'FrozenFoodGuy'

# Adjust these two fields to what Imgur provides.
client_id = 'Client-ID 1111111111111' # Replace 1111111111111 with your Client ID
client_token = 'Bearer 22222222222222222222222222222222222222222' # Replace 22222222222222222222222222222222222222222 with your Token

def get_count():
    ''' Retreive the number of comments '''
    comment_count_url = 'https://api.imgur.com/3/account/{}/comments/count'.format(username)
    r = requests.get(comment_count_url, headers={'Authorization': client_id})
    print(r.status_code)
    content = r.content
    content_str = content.decode("utf-8")
    content_json = json.loads(content_str)
    count = content_json['data']
    return count

def upvote_list():
    ''' Gather a list of comment IDs '''
    comment_count = get_count()
    page_count = math.ceil(comment_count / 50) # Querying the comment IDs only list 50 per page.
    comment_id_list = []
    page_number = 0
    while page_number < page_count:
        comment_id_url = 'https://api.imgur.com/3/account/{}/comments/ids/newest/{}'.format(username, page_number)
        r = requests.get(comment_id_url,  headers={'Authorization': client_id})
        content = r.content
        content_str = content.decode("utf-8")
        content_json = json.loads(content_str)
        lst = content_json['data']
        comment_id_list += lst
        page_number += 1
    return comment_id_list

def upvote(lst):
    ''' Execute Upvotes based on comment IDs '''
    fail_lst = []
    fail_count = 0
    pass_count = 0
    comment_id = lst[0]
    while len(lst) > 0:
        comment_upvote_url = 'https://api.imgur.com/3/comment/{}/vote/up'.format(comment_id)
        r = requests.get(comment_upvote_url,  headers={'Authorization': client_token})
        print(r.status_code)
        print(r.content)
        if r.status_code == 200:
            print('Upvote on Comment ID {} was successful'.format(lst[0]))
            lst.pop(0)
            pass_count += 1
        else:
            print('Upvote on Comment ID {} was unsuccessful'.format(lst[0]))
            fail_lst.append(lst[0])
            lst.pop(0)
            fail_count += 1
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Total Successful Upvotes:    {}'.format(pass_count))
    print('Total Failed Upvotes:        {}'.format(fail_count))
    print('List of Failed Comment IDs:')
    print(fail_lst)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def main():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~               FrozenFoodGuy                ~~')
    print('~~       Get Him to 10Million Upvotes!        ~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')
    print('Gathering Comment IDs...')
    id_list = upvote_list()
    print('Starting the upvote process...')
    upvote(id_list)

if __name__ == '__main__':
    main()
