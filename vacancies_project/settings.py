# main data settings
DATA_PATH = 'data/'

# hh parsing settings
HH_FILE = 'data_hh.json'
HH_URL = 'https://api.hh.ru/vacancies'
HH_AREA_PARAM = 113
HH_PER_PAGE = 100
HH_TOTAL_NUM = 1000
HH_MAX_RANGE = 11

# sj parsing settings
SJ_FILE = 'data_sj.json'
SJ_URL = 'https://russia.superjob.ru/vacancy/search/'
SJ_SOUP_CLASS = 'f-test-search-result-item'
SJ_HTML_ARTIFACTS = '<highlighttext>Python</highlighttext>'

# salary settings
NO_SALARY_LIST = ['По договорённости', 'не указано', 'None']
NO_SALARY = 'не указано'
