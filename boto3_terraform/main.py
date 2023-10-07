import boto3
import os
import subprocess
import pathlib
import json
import numpy

iam_client = boto3.client('iam')
iam_paginator = iam_client.get_paginator('list_users')
iam_paginate = iam_paginator.paginate()
mylist = []
for users in iam_paginate:
    # print(users)
    for all_users in users["Users"]:
        each_user = all_users["UserName"]
        mylist.append(each_user)
# print(mylist)
userslist = numpy.array(mylist)
numpy.savetxt('/Users/admin/Documents/ts-core-infra/tf.txt', userslist, delimiter=',', fmt='%s')
pathlib.Path("/Users/admin/Documents/ts-core-infra").mkdir(parents=True, exist_ok=True)


iam_roles_paginator = iam_client.list_roles()
# print(iam_roles_paginator)
myroles =[]
for roles in iam_roles_paginator['Roles']:
    # print(roles)
    #returns all the rolenames in the account
    rolers = roles['RoleName']
    #python uses {} to as format method for strings so i parsed it as a string so i can reference it the terraform code
    curly = "{}"
     #specify your desired path on your os inn my case i used /Users/admin/Documents/ts-core-infra
    pathlib.Path("/Users/admin/Documents/ts-core-infra/roles.tf").touch(exist_ok=True)
    terraformcode = "resource \"aws_iam_role\" \"{}\" {} \n"
    #formattiing the string
    newcode = terraformcode.format(rolers, curly)
    #specify your desired path on your os inn my case I used /Users/admin/Documents/ts-core-infra/roles.tf
    with open("/Users/admin/Documents/ts-core-infra/roles.tf", "a") as f:
        f.write(newcode)
    #this defines the terraform import code and makes it resuable
    importcode = "terraform import aws_iam_role.{} {}"
    codeallowed = importcode.format(rolers, rolers)
    os.system(codeallowed)
    #appending the roles to a list 
    myroles.append(rolers)
#writing the list of roles to a file
roles_file = numpy.array(myroles)
numpy.savetxt('/Users/admin/Documents/ts-core-infra/roles.txt', roles_file, delimiter=',', fmt='%s')
