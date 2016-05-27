# -*- coding: utf-8 -*-

import urllib2
import json
import numpy as np
import cPickle as pickle
from copy import deepcopy
from time import time

POIs = ['杭州市岳王庙', '杭州市灵隐寺', '杭州市宋城区', '杭州市雷峰塔', '杭州市西溪湿地', '杭州市杭州乐园',
		'杭州市九溪十八涧', '杭州市断桥', '杭州市清河坊', '杭州市三潭印月', '杭州市钱塘江', '杭州市孤山',
		'杭州市浙西大峡谷', '杭州市苏堤', '杭州市南山路', '杭州市曲院风荷', '杭州市六和塔', '杭州市湘湖',
		'杭州市杭州动物园', '杭州市西泠印社', '杭州市龙井村', '杭州市瑶琳仙境', '杭州市千岛湖森林氧吧',
		'杭州市浙江大学', '杭州市钱塘江大桥', '杭州市钱江新城', '杭州市龙门古镇', '杭州市极地海洋公园',
		'杭州市天目山', '杭州市杭州植物园', '杭州市平湖秋月', '杭州市柳浪闻莺', '杭州市飞来峰', '杭州市虎跑梦泉',
		'杭州市浙江省博物馆', '杭州市京杭大运河（杭州段）', '杭州市杭州野生动物世界', '杭州市海底世界', '杭州市太子湾']
POIs_copy = deepcopy(POIs)
numPOIs = len(POIs)
coordinates_POIs = np.zeros((numPOIs, 2))
distance_POIs = np.zeros((numPOIs, numPOIs)) + 0.001


def geocode_POI(POI, coord_type, area='杭州', AK = 'F75sheWie7rqeDLXjj96DPrKEQCxsOrl'):
	"""
	给定景点名称和经纬度返回形式，及景点所在区域，返回POI经纬度
	:param POI: 景点
	:param area: 景点所在区域
	:param coord_type: 经纬度坐标类型
	:return: POI名称及经纬度（包括POI附近的一些景点）
	"""
	path = 'http://api.map.baidu.com/place/v2/search?'
	param = 'query={0}&region={1}&city_limit=true&output=json&ak={2}&coord_type={3}'.format(POI, area, AK, coord_type)
	url_address = path + param
	try:
		content = urllib2.urlopen(url_address).read()
		geo_result = json.loads(content)
		POIs = []

		if geo_result['status'] == 0 and geo_result['message'] == 'ok':
			results = geo_result['results']
			num_results = len(results)
			for i in range(num_results):
				coors = results[i]['location']
				lat = coors['lat']
				lng = coors['lng']
				name = results[i]['name']
				address = results[i]['address']
				POIs.append((name, str(lat) + ',' + str(lng)))
		else:
			print 'status:', geo_result['status'], ';message:', geo_result['message']
			return None
		return POIs
	except urllib2.URLError, e:
		print e.reason
		return None

def get_distance_g(origins, destination):
	"""
	给定起止点，返回起止点间的距离
	:param origins: 出发点（可以是POI名称或者POI经纬度【字符串形式】）
	:param destination: 目的POI
	:return: 起止点距离
	"""
	key = 'AIzaSyA04pYbdn1dzt3Yxj5Gls74Vlilh_5FunA'
	path = 'https://maps.googleapis.com/maps/api/distancematrix/'
	param = 'json?origins={0}&destinations={1}&key='.format(origins, destination, key)
	url_address = path + param
	try:
		urlContent = urllib2.urlopen(url_address).read()
		getJSON = json.loads(urlContent)
		if getJSON['status'] == 'OK':
			# pass
			# OK 表示响应包含有效的 result
			# print origins + ' to ' + destination + ': ',
			distance,unit =  getJSON['rows'][0]['elements'][0]['distance']['text'].split(u' ')
			if unit == u'm':
				return  float(distance)/1000
			elif unit == u'km':
				return float(distance)
			# print origins + ' to ' + destination + ' need ' + 'time' + ': ',
			# print getJSON['rows'][0]['elements'][0]['duration']['text']
		elif getJSON['status'] == 'INVALID_REQUEST':
			# INVALID_REQUEST 表示提供的请求无效
			print '提供的请求无效'
			return None
		elif getJSON['status'] == 'MAX_ELEMENTS_EXCEEDED':
			# MAX_ELEMENTS_EXCEEDED 表示起点与目的地的乘积超过了每次查询限制
			print '起点与目的地的乘积超过了每次查询限制'
			return None
		elif getJSON['status'] == 'OVER_QUERY_LIMIT':
			# OVER_QUERY_LIMIT 表示服务在允许的时段内从您的应用收到的请求数量过多
			print '服务在允许的时段内从您的应用收到的请求数量过多'
			return None
		elif getJSON['status'] == 'REQUEST_DENIED':
			# REQUEST_DENIED 表示服务拒绝您的应用使用 Distance Matrix 服务
			print '服务拒绝您的应用使用 Distance Matrix 服务'
			return None
		elif getJSON['status'] == 'UNKNOWN_ERROR':
			# UNKNOWN_ERROR 表示由于服务器发生错误而无法处理 Distance Matrix 请求。如果您重试一次，请求可能会成功
			print '服务器发生错误而无法处理 Distance Matrix 请求。如果您重试一次，请求可能会成功'
			return None
	except urllib2.URLError, e:
		print e.reason
		return None

def get_distance_b(origins, destination, AK = 'F75sheWie7rqeDLXjj96DPrKEQCxsOrl'):
	path = 'http://api.map.baidu.com/direction/v1/routematrix?output=json&'
	param = 'origins={0}&destinations={1}&ak={2}'.format(origins, destination, AK)
	url_address = path + param
	try:
		urlContent = urllib2.urlopen(url_address).read()
		getJSON = json.loads(urlContent)
		if getJSON['status'] == 0:
			distance =  getJSON['result']['elements'][0]['distance']['value']
			return float(distance)/1000
		else:
			print 'status:', getJSON['status'], ';message:', getJSON['message']
			return None
	except urllib2.URLError, e:
		print e.reason
		return None

def coor_dis():
	for i in xrange(numPOIs):
		pois_i = geocode_POI(POIs[i], 2)

		for j in xrange(numPOIs):
			if i == j:
				continue
			pois_j = geocode_POI(POIs[j], 2)
			if pois_j == None:
				print 'POI名称出错: ', (i, j)
				continue
			distance = get_distance_b(pois_i[0][1], pois_j[0][1])
			if distance == None:
				print '计算POIs距离出错'
				continue
			distance_POIs[i][j] = distance

		if POIs[i].decode('utf8') != pois_i[0][0]:
			POIs_copy[i] = pois_i[0][0]
		lat, lng = pois_i[0][1].split(',')
		coordinates_POIs[i] = [float(lat), float(lng)]
		print i


if __name__ == '__main__':
	s = time()
	coor_dis()
	pickle.dump(coordinates_POIs, open('coordinates_POIs_new.pkl', 'w'))
	pickle.dump(distance_POIs, open('distance_POIs_new.pkl', 'w'))

	# get_distance_g(POIs[0], POIs[1])
	# print get_distance_b(POIs[7], POIs[32])
	print time()-s