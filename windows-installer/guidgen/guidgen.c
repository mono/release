#include <stdio.h>
#include <w32api/rpc.h>

int main()
{
	unsigned char *uuid_string;
	UUID my_uuid;
	RPC_STATUS status;
	
	status = UuidCreate(&my_uuid); 
	status = UuidToString(&my_uuid, &uuid_string);

	printf("%s", uuid_string);

	status = RpcStringFree(&uuid_string);

}
