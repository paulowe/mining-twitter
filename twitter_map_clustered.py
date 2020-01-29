from argparse import ArgumentParser
import folium
from folium.plugins import MarkerCluster
import json

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--geojson')
    parser.add_argument('--map')
    return parser

def make_map(geojson_file, map_file):

    tweet_map = folium.Map(Location=[50, 5], max_zoom=20)

    marker_cluster = MarkerCluster().add_to(tweet_map)

    geodata= json.load(open(geojson_file))

    for tweet in geodata['features']:
        tweet['geometry']['coordinates'].reverse()
        marker = folium.Marker(tweet['geometry']['coordinates'], popup=tweet['properties']['text'])
        marker.add_to(marker_cluster)

    #Save to HTML map file
    tweet_map.save(map_file)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    make_map(args.geojson, args.map)
