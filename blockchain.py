import random
import sys
import base64

import json

from web3 import Web3
from solcx import compile_standard

import solcx
solcx.install_solc()

compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "phb.sol": {
             "content": '''
                 pragma solidity >=0.4.0 <=0.8.15;
               

                contract PHB {

                    struct Employee
                    {                     
                        int id1;
                        string name;
                        string phone;
                        string address1;
                        string salary;
                    }

                    Employee []emps;

                    function addEmployee(int id1,string memory name, string memory address1,string memory phone, string memory salary) public
                    {
                        Employee memory e
                            =Employee(id1,
                                    name,
                                    address1,
                                    phone,
                                    salary);
                        emps.push(e);
                    }

                    function getEmployee(int id1) public view returns(
                            string memory, 
                            string memory, 
                            string memory,
                            string memory
                            
                            )
                    {
                        uint i;
                        for(i=emps.length-1;i>0;i--)
                        {
                            Employee memory e
                                =emps[i];
                            
                            if(e.id1==id1)
                            {
                                return(e.name,
                                    e.address1,
                                    e.phone,
                                    e.salary
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               
                               );
                    }

                    function getEmployeeCount() public view returns(uint256)
                    {
                        return(emps.length);
                    }

                    struct Logs
                    {
                        int log_id;
                        string log_details;
                    }
                    Logs []my_logs;

                    function addLogs(int log_id,string memory log_details) public
                    {
                        Logs memory l
                            =Logs(log_id,
                                    log_details);
                        my_logs.push(l);
                    }

       
                }

               '''
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
 })


# web3.py instance



def verify_key(adr1,key):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr1,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(0.1, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        return True
    except Exception as e:
        print(e)  
        return False  



def create_contract():
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # get bytecode
    bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    pb = w3.eth.contract(abi=abi, bytecode=bytecode)

    # # Submit the transaction that deploys the contract
    tx_hash = pb.constructor().transact()

    # # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print("tx_receipt.contractAddress: ",tx_receipt.contractAddress)
    f=open('contract_address.txt','w')
    f.write(tx_receipt.contractAddress)
    f.close()

def add_logs(log_id,log_details):
    f=open('contract_address.txt','r')
    address1=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[1]
    print(type(w3.eth.accounts[1]))

    # get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address1,
        abi=abi
    )
   
    tx_hash = p1.functions.addLogs(int(log_id),log_details).transact()
    



def add_employee1(id,name,address,phone,salary):
    f=open('contract_address.txt','r')
    address1=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address1,
        abi=abi
    )
   
    tx_hash = p1.functions.addEmployee(int(id),name,address,phone,salary).transact()
    

    #print(tx_hash) 
   
    

    

def get_employee(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getEmployee(id1).call()
    print(store)
    return store


def get_contract():
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount =  w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    return p1



def verify_adr(s):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    adrs = w3.eth.accounts
    print(adrs)

    if s in adrs:
        return True
    else:
        return False    





if __name__=="__main__":
    
    
    #save_to_block(5)
    create_contract()
    add_employee1(0,'he','he','he','he')    #it is essential when creating contract
    # get_employee(0)
    # c=get_patient_count()
    # print(c)
    # for i in range(1,10):
    #     print(i)
    #     get_employee(i)

    #get_doctor(1)
    #allow(5,'0x3529A6ee990639C32bEe5F841a9649cdd0c6e0FD')
    #get_allowed(5)
    #print(verify_adr('0xED8E36D67cD35E2F863E2f7EF90570bb543e60a0'))
    #assign(1,2)
    #verify_transaction('0xc54ff78d3e21b45e072351a02bcc4758659d0497e3f9b34dfd7faeb1cd4be073')
    
    #payment('0xB8b84d25a3eaEf0d231D9E422DdE7B21839E6793','0x44b2c1e452B5AA05235cB040773111DE30d53B0f','82a2f61beebb41befafb032060ad6108ba3178c240fdcace93325bca1b6db992','300')