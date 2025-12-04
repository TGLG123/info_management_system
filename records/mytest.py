from web3 import Web3

# 使用测试网 RPC 地址
CONFLUX_TESTNET_RPC = "https://test.confluxrpc.com"

# 初始化 Web3
web3 = Web3(Web3.HTTPProvider(CONFLUX_TESTNET_RPC))

# 测试连接
try:
    print("正在测试与 Conflux RPC 的连接...")
    response = web3.provider.make_request("cfx_epochNumber", [])
    print("RPC 响应:", response)

    # 检查响应是否包含错误
    if "error" in response:
        print("RPC 响应中包含错误:", response["error"])
    else:
        epoch_number_hex = response["result"]  # 获取十六进制的 epoch
        epoch_number = int(epoch_number_hex, 16)  # 转换为十进制
        print("当前 Epoch（十进制）:", epoch_number)  # 打印十进制的区块高度
except Exception as e:
    print("无法连接到 RPC 服务:", e)
