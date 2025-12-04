# #blockchain_config.py
# from web3 import Web3
# import base64
# import traceback  # 用于打印详细错误堆栈
#
# # 配置
# PRIVATE_KEY = "735820882fe23c86009feb9988926f3106af6cd46af855ca9fa23ffb1f01ba1b"  # 替换为你的私钥
# ACCOUNT_ADDRESS = "cfxtest:aankxr6ueysgrp5dc1wh8mk91hsuaenpmec0sx2nwr"  # 替换为你的 Conflux 地址
# CONFLUX_TESTNET_RPC = "https://test.confluxrpc.com"  # Conflux 测试网地址
#
# # 地址转换函数
# def to_conflux_base32(eth_address: str, network_id: int = 1029) -> str:
#     if not eth_address.startswith("0x") or len(eth_address) != 42:
#         raise ValueError(f"无效的以太坊地址格式: {eth_address}")
#     eth_address_bytes = bytes.fromhex(eth_address[2:])
#     prefix = "cfxtest" if network_id == 1029 else "cfx"
#     payload = b"\x00" + eth_address_bytes
#     base32_address = base64.b32encode(payload).decode("utf-8").lower().replace("=", "")
#     return f"{prefix}:{base32_address}"
#
# try:
#     print("正在连接到 Conflux 测试网...")
#     web3 = Web3(Web3.HTTPProvider(CONFLUX_TESTNET_RPC))
#
#     # 用 cfx_epochNumber 方法验证连接
#     try:
#         print("正在调用 RPC 方法 'cfx_epochNumber' 验证连接...")
#         epoch_number = web3.manager.request_blocking("cfx_epochNumber", [])
#         print(f"成功连接到 Conflux 测试网，当前 Epoch: {int(epoch_number, 16)}")
#     except Exception as rpc_error:
#         raise ConnectionError(f"无法连接到 Conflux 测试网或 RPC 返回错误: {rpc_error}")
#
#     # 使用私钥生成以太坊地址
#     print(f"正在使用私钥生成以太坊地址...")
#     account = web3.eth.account.from_key(PRIVATE_KEY)
#     eth_address = account.address  # 以太坊格式地址
#     print(f"生成的以太坊地址: {eth_address}")
#
#     # 转换为 Conflux 地址格式
#     print(f"正在将以太坊地址转换为 Conflux 格式地址...")
#     generated_address = to_conflux_base32(eth_address, network_id=1029)
#     print(f"转换后的 Conflux 地址: {generated_address}")
#
#     # 比较 Conflux 地址是否匹配
#     print(f"正在比较生成的地址与配置的地址是否一致...")
#     if generated_address != ACCOUNT_ADDRESS:
#         raise ValueError(
#             f"私钥与钱包地址不匹配。\n生成的地址: {generated_address}\n配置的地址: {ACCOUNT_ADDRESS}"
#         )
#
#     print("地址验证成功，私钥与 Conflux 地址匹配")
#
# except ValueError as ve:
#     print(f"配置或格式化错误: {ve}")
# except ConnectionError as ce:
#     print(f"连接错误: {ce}")
# except Exception as e:
#     print(f"区块链初始化时发生未知错误: {e}")
#     traceback.print_exc()  # 打印详细错误堆栈








# from conflux_web3 import Web3
#
# # 区块链连接配置
# TESTNET_RPC_URL = "https://testnet.confluxrpc.com"
# web3 = Web3(Web3.HTTPProvider(TESTNET_RPC_URL))
#
# # 账户配置
# ACCOUNT_ADDRESS = "cfxtest:aankxr6ueysgrp5dc1wh8mk91hsuaenpmec0sx2nwr"  # 从 Fluent Wallet 获取
# PRIVATE_KEY = "735820882fe23c86009feb9988926f3106af6cd46af855ca9fa23ffb1f01ba1b"  # 从 Fluent Wallet 导出
#
# def send_to_blockchain(data):
#     """
#     将 JSON 数据编码为区块链交易的 data 字段并发送交易
#     """
#     try:
#         # 将数据编码为 Hex 格式
#         encoded_data = web3.toHex(text=data)
#
#         # 构造交易
#         transaction = {
#             "from": ACCOUNT_ADDRESS,
#             "to": ACCOUNT_ADDRESS,  # 可替换为智能合约地址
#             "value": 0,  # 不转移 CFX，仅存储数据
#             "gas": 50000,  # 根据数据大小调整 Gas
#             "gasPrice": web3.cfx.gas_price,
#             "data": encoded_data,
#             "nonce": web3.cfx.get_next_nonce(ACCOUNT_ADDRESS),
#         }
#
#         # 签名交易
#         signed_tx = web3.account.sign_transaction(transaction, PRIVATE_KEY)
#
#         # 发送交易到区块链
#         tx_hash = web3.cfx.send_raw_transaction(signed_tx.rawTransaction)
#         return tx_hash.hex()  # 返回交易哈希
#     except Exception as e:
#         print(f"发送区块链交易失败: {e}")
#         return None
