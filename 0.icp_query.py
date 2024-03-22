# 通过接口查询域名或公司备案

import yaml
from lib.logo import logo
from lib.Requests_func import make_request
from argparse import ArgumentParser

def query_from(query_url, search_data):
    params = {
        'search': search_data,
    }
    req_list = make_request(query_url, params, search_data)
    if req_list:
        unitName_list = make_request(query_url, params, req_list[0]['unitName'])
        if unitName_list:
            for item in unitName_list:
                if item.get('domain') and item.get('unitName'):
                    output = f"unitName:{item['unitName']}, domain:{item['domain']}"
                    print(output)
                    open('log/success.log', 'a+', encoding='utf-8').write(str(output)+'\n')
                else:
                    print("unitName or domain is None...")
        else:
            print(f"No unitName_list found for {req_list}. Skipping...")
    else:
        print(f"No req_list found for {search_data}. Skipping...")
        open('log/no_req_list.log', 'a+', encoding='utf-8').write(search_data+'\n')

def query_from_file(query_url, filename, start_index):
    with open(filename, 'r', encoding='utf-8') as file:
        data_list = file.readlines()
        total_domains = len(data_list)
    if start_index < 1:
        start_index = 1
        print("输入异常, start_index 重置为 1")
    elif start_index > total_domains:
        start_index = total_domains
        print(f"输入异常, start_index 重置为 {total_domains}")
        
    for index in range(start_index-1, total_domains):
        data = data_list[index].strip()
        if data:
            print(f"\nProcessing Domain {index+1}/{total_domains}: {data}\n")
            open('log/Processing_Domain.log', 'a+', encoding='utf-8').write(f"{index+1}/{total_domains}: {data}\n")
            query_from(query_url, data)

if __name__ == '__main__':
    logo()
    parser = ArgumentParser()
    parser.add_argument("-d", dest="query_url", help="请输入测试平台地址")
    parser.add_argument("-u", dest="domain", help="请输入目标")
    parser.add_argument("-uf", dest="domains_file", help="请输入目标文件")
    parser.add_argument("-s", dest="start_index", type=int, default="1", help="请输入起始位置，第一个数据的下标为0")
    args = parser.parse_args()

    # Load YAML configuration
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    if args.query_url:
        if args.domain:
            # 执行查询
            query_from(args.query_url, args.domain)
        elif args.domains_file:
            print(f"Query_urls: {args.query_url}\nDomains_file: {args.domains_file}")
            query_from_file(args.query_url, args.domains_file, args.start_index)
        else:
            print(f"Query_urls: {args.query_url}\nDomains_file: {push_config['domains_file']}")
            query_from_file(args.query_url, push_config['domains_file'], args.start_index)
    else:
        if args.domain:
            # 执行查询
            query_from(args.query_url, args.domain)
        elif args.domains_file:
            print(f"Query_urls: {push_config['query_url']}\nDomains_file: {args.domains_file}")
            query_from_file(push_config['query_url'], args.domains_file, args.start_index)
        else:
            print(f"Query_urls: {push_config['query_url']}\nDomains_file: {push_config['domains_file']}")
            query_from_file(push_config['query_url'], push_config['domains_file'], args.start_index)