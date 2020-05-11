from datetime import datetime

from colour_puller.database import AlbumDatabase
from tweetbot import TweetBot

print(datetime.now())

ad = AlbumDatabase()

album = ad.get_from_queue()

try:
    ad.update_album(album, status='processing')

    original, revised, palette = album.get_images()
    colour_codes = ', '.join(album.album_palette.hex_colours)

    tb = TweetBot(
        key_source='files', 
        consumer_key=r'tokens/consumer_key', 
        consumer_secret=r'tokens/consumer_secret',
        access_token=r'tokens/access_token', 
        access_token_secret=r'tokens/access_token_secret'
    )

    first_tweet = tb.post_photo(
        tweet_text=str(album), media=[revised, original], many=True
    )

    second_tweet = tb.post_photo(
        tweet_text=f'Colour hex codes: {colour_codes}',
        media=palette, many=False, in_reply_to_status_id=first_tweet['id']
    )

    ad.update_album(album, status='completed')

except:
    ad.update_album(album, status='processing')
