-- 插入全球地区数据（用于运费和关税分组）
-- 执行时间: 2025-06-25 17:17:48

-- 清空现有数据（如果需要重新导入）
-- DELETE FROM country_regions;
-- DELETE FROM region_translations;
-- DELETE FROM regions;

-- 插入地区数据
INSERT INTO regions (code, name, description, status) VALUES
('ASIA', 'Asia', 'Asian countries and territories', 'active'),
('EUROPE', 'Europe', 'European countries and territories', 'active'),
('NORTH_AMERICA', 'North America', 'North American countries and territories', 'active'),
('SOUTH_AMERICA', 'South America', 'South American countries and territories', 'active'),
('AFRICA', 'Africa', 'African countries and territories', 'active'),
('OCEANIA', 'Oceania', 'Oceanic countries and territories', 'active'),
('MIDDLE_EAST', 'Middle East', 'Middle Eastern countries', 'active'),
('CENTRAL_ASIA', 'Central Asia', 'Central Asian countries', 'active'),
('CARIBBEAN', 'Caribbean', 'Caribbean countries and territories', 'active'),
('SOUTHEAST_ASIA', 'Southeast Asia', 'Southeast Asian countries (ASEAN region)', 'active'),
('EAST_ASIA', 'East Asia', 'East Asian countries (China, Japan, Korea, etc.)', 'active'),
('WESTERN_EUROPE', 'Western Europe', 'Western European countries', 'active'),
('EASTERN_EUROPE', 'Eastern Europe', 'Eastern European countries', 'active'),
('NORTHERN_EUROPE', 'Northern Europe', 'Northern European countries (Nordic region)', 'active'),
('SOUTHERN_EUROPE', 'Southern Europe', 'Southern European countries (Mediterranean region)', 'active'),
('NORTH_AFRICA', 'North Africa', 'North African countries', 'active'),
('WEST_AFRICA', 'West Africa', 'West African countries', 'active'),
('EAST_AFRICA', 'East Africa', 'East African countries', 'active'),
('SOUTHERN_AFRICA', 'Southern Africa', 'Southern African countries', 'active'),
('CENTRAL_AFRICA', 'Central Africa', 'Central African countries', 'active'),
('DEVELOPED', 'Developed Countries', 'Developed economies with lower shipping costs', 'active'),
('DEVELOPING', 'Developing Countries', 'Developing economies with standard shipping costs', 'active'),
('REMOTE_ISLANDS', 'Remote Islands', 'Remote island territories with higher shipping costs', 'active'),
('EU', 'European Union', 'European Union member countries', 'active'),
('NAFTA', 'USMCA', 'United States-Mexico-Canada Agreement countries', 'active'),
('ASEAN', 'ASEAN', 'Association of Southeast Asian Nations', 'active'),
('GCC', 'Gulf Cooperation Council', 'Gulf Cooperation Council member countries', 'active'),
('MERCOSUR', 'Mercosur', 'Southern Common Market countries', 'active'),
('AU', 'African Union', 'African Union member countries', 'active'),
('SAARC', 'SAARC', 'South Asian Association for Regional Cooperation', 'active');

-- 插入地区中文翻译
INSERT INTO region_translations (region_id, language, name, description) VALUES
((SELECT id FROM regions WHERE code = 'ASIA'), 'zh-CN', '亚洲', '亚洲国家和地区'),
((SELECT id FROM regions WHERE code = 'EUROPE'), 'zh-CN', '欧洲', '欧洲国家和地区'),
((SELECT id FROM regions WHERE code = 'NORTH_AMERICA'), 'zh-CN', '北美洲', '北美洲国家和地区'),
((SELECT id FROM regions WHERE code = 'SOUTH_AMERICA'), 'zh-CN', '南美洲', '南美洲国家和地区'),
((SELECT id FROM regions WHERE code = 'AFRICA'), 'zh-CN', '非洲', '非洲国家和地区'),
((SELECT id FROM regions WHERE code = 'OCEANIA'), 'zh-CN', '大洋洲', '大洋洲国家和地区'),
((SELECT id FROM regions WHERE code = 'MIDDLE_EAST'), 'zh-CN', '中东', '中东国家'),
((SELECT id FROM regions WHERE code = 'CENTRAL_ASIA'), 'zh-CN', '中亚', '中亚国家'),
((SELECT id FROM regions WHERE code = 'CARIBBEAN'), 'zh-CN', '加勒比海地区', '加勒比海国家和地区'),
((SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA'), 'zh-CN', '东南亚', '东南亚国家（东盟地区）'),
((SELECT id FROM regions WHERE code = 'EAST_ASIA'), 'zh-CN', '东亚', '东亚国家（中日韩等）'),
((SELECT id FROM regions WHERE code = 'WESTERN_EUROPE'), 'zh-CN', '西欧', '西欧国家'),
((SELECT id FROM regions WHERE code = 'EASTERN_EUROPE'), 'zh-CN', '东欧', '东欧国家'),
((SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE'), 'zh-CN', '北欧', '北欧国家（北欧地区）'),
((SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE'), 'zh-CN', '南欧', '南欧国家（地中海地区）'),
((SELECT id FROM regions WHERE code = 'NORTH_AFRICA'), 'zh-CN', '北非', '北非国家'),
((SELECT id FROM regions WHERE code = 'WEST_AFRICA'), 'zh-CN', '西非', '西非国家'),
((SELECT id FROM regions WHERE code = 'EAST_AFRICA'), 'zh-CN', '东非', '东非国家'),
((SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA'), 'zh-CN', '南非地区', '南非地区国家'),
((SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA'), 'zh-CN', '中非', '中非国家'),
((SELECT id FROM regions WHERE code = 'DEVELOPED'), 'zh-CN', '发达国家', '发达经济体，运费较低'),
((SELECT id FROM regions WHERE code = 'DEVELOPING'), 'zh-CN', '发展中国家', '发展中经济体，标准运费'),
((SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS'), 'zh-CN', '偏远岛屿', '偏远岛屿地区，运费较高'),
((SELECT id FROM regions WHERE code = 'EU'), 'zh-CN', '欧盟', '欧盟成员国'),
((SELECT id FROM regions WHERE code = 'NAFTA'), 'zh-CN', '美墨加协定', '美国-墨西哥-加拿大协定国家'),
((SELECT id FROM regions WHERE code = 'ASEAN'), 'zh-CN', '东盟', '东南亚国家联盟'),
((SELECT id FROM regions WHERE code = 'GCC'), 'zh-CN', '海湾合作委员会', '海湾合作委员会成员国'),
((SELECT id FROM regions WHERE code = 'MERCOSUR'), 'zh-CN', '南方共同市场', '南方共同市场国家'),
((SELECT id FROM regions WHERE code = 'AU'), 'zh-CN', '非洲联盟', '非洲联盟成员国'),
((SELECT id FROM regions WHERE code = 'SAARC'), 'zh-CN', '南亚区域合作联盟', '南亚区域合作联盟');

-- 插入国家地区关联关系
INSERT INTO country_regions (country_id, region_id) VALUES
-- 东亚地区
((SELECT id FROM countries WHERE code = 'CN'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'CN'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'CN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'JP'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'JP'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'JP'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'KR'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'KR'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'KR'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'TW'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'TW'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'TW'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'HK'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'HK'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'HK'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'MO'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'MO'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'MO'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'MN'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'MN'), (SELECT id FROM regions WHERE code = 'EAST_ASIA')),
((SELECT id FROM countries WHERE code = 'MN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 东南亚地区（东盟国家）
((SELECT id FROM countries WHERE code = 'TH'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'TH'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'TH'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'TH'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'VN'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'VN'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'VN'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'VN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MY'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'MY'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'MY'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'MY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SG'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'SG'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'SG'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'SG'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'ID'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'ID'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'ID'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'ID'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'PH'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'PH'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'PH'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'PH'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MM'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'MM'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'MM'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'MM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'KH'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'KH'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'KH'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'KH'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LA'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'LA'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'LA'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'LA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BN'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'BN'), (SELECT id FROM regions WHERE code = 'SOUTHEAST_ASIA')),
((SELECT id FROM countries WHERE code = 'BN'), (SELECT id FROM regions WHERE code = 'ASEAN')),
((SELECT id FROM countries WHERE code = 'BN'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

-- 南亚地区（SAARC国家）
((SELECT id FROM countries WHERE code = 'IN'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'IN'), (SELECT id FROM regions WHERE code = 'SAARC')),
((SELECT id FROM countries WHERE code = 'IN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BD'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'BD'), (SELECT id FROM regions WHERE code = 'SAARC')),
((SELECT id FROM countries WHERE code = 'BD'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'PK'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'PK'), (SELECT id FROM regions WHERE code = 'SAARC')),
((SELECT id FROM countries WHERE code = 'PK'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LK'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'LK'), (SELECT id FROM regions WHERE code = 'SAARC')),
((SELECT id FROM countries WHERE code = 'LK'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'NP'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'NP'), (SELECT id FROM regions WHERE code = 'SAARC')),
((SELECT id FROM countries WHERE code = 'NP'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 中东地区（GCC国家）
((SELECT id FROM countries WHERE code = 'SA'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'SA'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'SA'), (SELECT id FROM regions WHERE code = 'GCC')),
((SELECT id FROM countries WHERE code = 'SA'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'AE'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'AE'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'AE'), (SELECT id FROM regions WHERE code = 'GCC')),
((SELECT id FROM countries WHERE code = 'AE'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'KW'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'KW'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'KW'), (SELECT id FROM regions WHERE code = 'GCC')),
((SELECT id FROM countries WHERE code = 'KW'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'QA'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'QA'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'QA'), (SELECT id FROM regions WHERE code = 'GCC')),
((SELECT id FROM countries WHERE code = 'QA'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'BH'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'BH'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'BH'), (SELECT id FROM regions WHERE code = 'GCC')),
((SELECT id FROM countries WHERE code = 'BH'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'OM'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'OM'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'OM'), (SELECT id FROM regions WHERE code = 'GCC')),
((SELECT id FROM countries WHERE code = 'OM'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

-- 其他中东国家
((SELECT id FROM countries WHERE code = 'IR'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'IR'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'IR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'IQ'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'IQ'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'IQ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'JO'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'JO'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'JO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LB'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'LB'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'LB'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SY'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'SY'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'SY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'YE'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'YE'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'YE'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'IL'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'IL'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'IL'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'PS'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'PS'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'PS'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TR'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'TR'), (SELECT id FROM regions WHERE code = 'MIDDLE_EAST')),
((SELECT id FROM countries WHERE code = 'TR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 中亚国家
((SELECT id FROM countries WHERE code = 'UZ'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'UZ'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'UZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'KZ'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'KZ'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'KZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'KG'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'KG'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'KG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TJ'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'TJ'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'TJ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TM'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'TM'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'TM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AM'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'AM'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'AM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AZ'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'AZ'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'AZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GE'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'GE'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'GE'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AF'), (SELECT id FROM regions WHERE code = 'ASIA')),
((SELECT id FROM countries WHERE code = 'AF'), (SELECT id FROM regions WHERE code = 'CENTRAL_ASIA')),
((SELECT id FROM countries WHERE code = 'AF'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 西欧国家（EU成员）
((SELECT id FROM countries WHERE code = 'DE'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'DE'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'DE'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'DE'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'FR'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'FR'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'FR'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'FR'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'IT'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'IT'), (SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'IT'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'IT'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'ES'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'ES'), (SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'ES'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'ES'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'NL'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'NL'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'NL'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'NL'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'BE'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'BE'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'BE'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'BE'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'AT'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'AT'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'AT'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'AT'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'LU'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'LU'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'LU'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'LU'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'CH'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'CH'), (SELECT id FROM regions WHERE code = 'WESTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'CH'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'GB'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'GB'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'GB'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'IE'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'IE'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'IE'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'IE'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

-- 北欧国家
((SELECT id FROM countries WHERE code = 'SE'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'SE'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'SE'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'SE'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'NO'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'NO'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'NO'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'DK'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'DK'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'DK'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'DK'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'FI'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'FI'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'FI'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'FI'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'IS'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'IS'), (SELECT id FROM regions WHERE code = 'NORTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'IS'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

-- 南欧国家
((SELECT id FROM countries WHERE code = 'PT'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'PT'), (SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'PT'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'PT'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'GR'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'GR'), (SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'GR'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'GR'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'MT'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'MT'), (SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'MT'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'MT'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'CY'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'CY'), (SELECT id FROM regions WHERE code = 'SOUTHERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'CY'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'CY'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

-- 东欧国家
((SELECT id FROM countries WHERE code = 'PL'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'PL'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'PL'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'PL'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'CZ'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'CZ'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'CZ'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'CZ'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'SK'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'SK'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'SK'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'SK'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'HU'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'HU'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'HU'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'HU'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'RO'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'RO'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'RO'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'RO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BG'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'BG'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'BG'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'BG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'HR'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'HR'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'HR'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'HR'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'SI'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'SI'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'SI'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'SI'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'LT'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'LT'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'LT'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'LT'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'LV'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'LV'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'LV'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'LV'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'EE'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'EE'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'EE'), (SELECT id FROM regions WHERE code = 'EU')),
((SELECT id FROM countries WHERE code = 'EE'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'RU'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'RU'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'RU'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'UA'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'UA'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'UA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BY'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'BY'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'BY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MD'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'MD'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'MD'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'RS'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'RS'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'RS'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BA'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'BA'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'BA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ME'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'ME'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'ME'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MK'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'MK'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'MK'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AL'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'AL'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'AL'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'XK'), (SELECT id FROM regions WHERE code = 'EUROPE')),
((SELECT id FROM countries WHERE code = 'XK'), (SELECT id FROM regions WHERE code = 'EASTERN_EUROPE')),
((SELECT id FROM countries WHERE code = 'XK'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 北美洲国家（NAFTA/USMCA）
((SELECT id FROM countries WHERE code = 'US'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'US'), (SELECT id FROM regions WHERE code = 'NAFTA')),
((SELECT id FROM countries WHERE code = 'US'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'CA'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'CA'), (SELECT id FROM regions WHERE code = 'NAFTA')),
((SELECT id FROM countries WHERE code = 'CA'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'MX'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'MX'), (SELECT id FROM regions WHERE code = 'NAFTA')),
((SELECT id FROM countries WHERE code = 'MX'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 中美洲国家
((SELECT id FROM countries WHERE code = 'GT'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'GT'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BZ'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'BZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SV'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'SV'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'HN'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'HN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'NI'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'NI'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CR'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'CR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'PA'), (SELECT id FROM regions WHERE code = 'NORTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'PA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 南美洲国家（包括MERCOSUR）
((SELECT id FROM countries WHERE code = 'BR'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'BR'), (SELECT id FROM regions WHERE code = 'MERCOSUR')),
((SELECT id FROM countries WHERE code = 'BR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AR'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'AR'), (SELECT id FROM regions WHERE code = 'MERCOSUR')),
((SELECT id FROM countries WHERE code = 'AR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'PY'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'PY'), (SELECT id FROM regions WHERE code = 'MERCOSUR')),
((SELECT id FROM countries WHERE code = 'PY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'UY'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'UY'), (SELECT id FROM regions WHERE code = 'MERCOSUR')),
((SELECT id FROM countries WHERE code = 'UY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CL'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'CL'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'PE'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'PE'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CO'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'CO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'VE'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'VE'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'EC'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'EC'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BO'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'BO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GY'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'GY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SR'), (SELECT id FROM regions WHERE code = 'SOUTH_AMERICA')),
((SELECT id FROM countries WHERE code = 'SR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 非洲国家（分区域）

-- 北非国家
((SELECT id FROM countries WHERE code = 'EG'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'EG'), (SELECT id FROM regions WHERE code = 'NORTH_AFRICA')),
((SELECT id FROM countries WHERE code = 'EG'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'EG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LY'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'LY'), (SELECT id FROM regions WHERE code = 'NORTH_AFRICA')),
((SELECT id FROM countries WHERE code = 'LY'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'LY'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TN'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'TN'), (SELECT id FROM regions WHERE code = 'NORTH_AFRICA')),
((SELECT id FROM countries WHERE code = 'TN'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'TN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'DZ'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'DZ'), (SELECT id FROM regions WHERE code = 'NORTH_AFRICA')),
((SELECT id FROM countries WHERE code = 'DZ'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'DZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MA'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'MA'), (SELECT id FROM regions WHERE code = 'NORTH_AFRICA')),
((SELECT id FROM countries WHERE code = 'MA'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'MA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SD'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'SD'), (SELECT id FROM regions WHERE code = 'NORTH_AFRICA')),
((SELECT id FROM countries WHERE code = 'SD'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'SD'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 西非国家
((SELECT id FROM countries WHERE code = 'NG'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'NG'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'NG'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'NG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GH'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'GH'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'GH'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'GH'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SN'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'SN'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'SN'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'SN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ML'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ML'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'ML'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ML'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BF'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'BF'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'BF'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'BF'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'NE'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'NE'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'NE'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'NE'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CI'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'CI'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'CI'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'CI'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LR'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'LR'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'LR'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'LR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SL'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'SL'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'SL'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'SL'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GN'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'GN'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'GN'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'GN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GW'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'GW'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'GW'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'GW'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GM'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'GM'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'GM'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'GM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CV'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'CV'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'CV'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'CV'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'CV'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MR'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'MR'), (SELECT id FROM regions WHERE code = 'WEST_AFRICA')),
((SELECT id FROM countries WHERE code = 'MR'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'MR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 东非国家
((SELECT id FROM countries WHERE code = 'KE'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'KE'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'KE'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'KE'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'UG'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'UG'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'UG'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'UG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TZ'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'TZ'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'TZ'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'TZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'RW'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'RW'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'RW'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'RW'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BI'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'BI'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'BI'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'BI'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ET'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ET'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'ET'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ET'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ER'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ER'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'ER'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ER'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'DJ'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'DJ'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'DJ'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'DJ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SO'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'SO'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'SO'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'SO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 南非地区国家
((SELECT id FROM countries WHERE code = 'ZA'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ZA'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'ZA'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ZA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ZW'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ZW'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'ZW'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ZW'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BW'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'BW'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'BW'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'BW'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ZM'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ZM'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'ZM'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ZM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MW'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'MW'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'MW'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'MW'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MZ'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'MZ'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'MZ'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'MZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'NA'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'NA'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'NA'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'NA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SZ'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'SZ'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'SZ'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'SZ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LS'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'LS'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'LS'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'LS'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AO'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'AO'), (SELECT id FROM regions WHERE code = 'SOUTHERN_AFRICA')),
((SELECT id FROM countries WHERE code = 'AO'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'AO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 中非国家
((SELECT id FROM countries WHERE code = 'CM'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'CM'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'CM'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'CM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CF'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'CF'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'CF'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'CF'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TD'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'TD'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'TD'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'TD'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GA'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'GA'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'GA'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'GA'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GQ'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'GQ'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'GQ'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'GQ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CG'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'CG'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'CG'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'CG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CD'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'CD'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'CD'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'CD'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'ST'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'ST'), (SELECT id FROM regions WHERE code = 'CENTRAL_AFRICA')),
((SELECT id FROM countries WHERE code = 'ST'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'ST'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'ST'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 印度洋岛屿国家
((SELECT id FROM countries WHERE code = 'MG'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'MG'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'MG'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'MG'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'MG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MU'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'MU'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'MU'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'MU'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'MU'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SC'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'SC'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'SC'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'SC'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'SC'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'KM'), (SELECT id FROM regions WHERE code = 'AFRICA')),
((SELECT id FROM countries WHERE code = 'KM'), (SELECT id FROM regions WHERE code = 'EAST_AFRICA')),
((SELECT id FROM countries WHERE code = 'KM'), (SELECT id FROM regions WHERE code = 'AU')),
((SELECT id FROM countries WHERE code = 'KM'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'KM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 大洋洲国家
((SELECT id FROM countries WHERE code = 'AU'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'AU'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'NZ'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'NZ'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'FJ'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'FJ'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'FJ'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'PG'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'PG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'SB'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'SB'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'SB'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'VU'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'VU'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'VU'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'NC'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'NC'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'NC'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'PF'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'PF'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'PF'), (SELECT id FROM regions WHERE code = 'DEVELOPED')),

((SELECT id FROM countries WHERE code = 'WS'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'WS'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'WS'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TO'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'TO'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'TO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'KI'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'KI'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'KI'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TV'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'TV'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'TV'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'NR'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'NR'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'NR'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'PW'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'PW'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'PW'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'FM'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'FM'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'FM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'MH'), (SELECT id FROM regions WHERE code = 'OCEANIA')),
((SELECT id FROM countries WHERE code = 'MH'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'MH'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

-- 加勒比海地区
((SELECT id FROM countries WHERE code = 'JM'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'JM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'CU'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'CU'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'HT'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'HT'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'DO'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'DO'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'TT'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'TT'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BB'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'BB'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'BB'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'LC'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'LC'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'LC'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'GD'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'GD'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'GD'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'VC'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'VC'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'VC'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'AG'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'AG'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'AG'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'DM'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'DM'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'DM'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'KN'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'KN'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'KN'), (SELECT id FROM regions WHERE code = 'DEVELOPING')),

((SELECT id FROM countries WHERE code = 'BS'), (SELECT id FROM regions WHERE code = 'CARIBBEAN')),
((SELECT id FROM countries WHERE code = 'BS'), (SELECT id FROM regions WHERE code = 'REMOTE_ISLANDS')),
((SELECT id FROM countries WHERE code = 'BS'), (SELECT id FROM regions WHERE code = 'DEVELOPING'));

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_country_regions_country_region ON country_regions(country_id, region_id);

-- 数据插入完成提示
SELECT 'Global regions data inserted successfully with country associations' as status;