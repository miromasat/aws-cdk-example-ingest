from aws_cdk import core, aws_dynamodb, aws_lambda, aws_apigateway


class CdkExampleIngestStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        partition_key_name = "driver_id"
        partition_key_type = aws_dynamodb.AttributeType.STRING
        sort_key_name = 'driver_setting'
        sort_key_type = aws_dynamodb.AttributeType.STRING

        
        configTable = aws_dynamodb.Table(self,  id='configTable', 
                                                table_name='configTable', 
                                                partition_key=aws_dynamodb.Attribute(name=partition_key_name, type=partition_key_type),
                                                sort_key=aws_dynamodb.Attribute(name=sort_key_name, type=sort_key_type))

        saveConfigFunction = aws_lambda.Function(self,  id='saveConfigFunction', 
                                                        runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                        handler='saveConfig.main',
                                                        code=aws_lambda.Code.asset('./lambda'))
        
        getConfigFunction = aws_lambda.Function(self,   id='getConfigFunction',
                                                        runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                        handler='getConfig.main',
                                                        code=aws_lambda.Code.asset('./lambda'))
        
        configTable.grant_read_data(getConfigFunction)
        configTable.grant_write_data(saveConfigFunction)

        saveConfigFunction.add_environment(key='TABLE_NAME', value=configTable.table_name)
        saveConfigFunction.add_environment(key='PARTITION_KEY_NAME', value=partition_key_name)
        saveConfigFunction.add_environment(key='SORT_KEY_NAME', value=sort_key_name)
        getConfigFunction.add_environment(key='TABLE_NAME', value=configTable.table_name)
        getConfigFunction.add_environment(key='PARTITION_KEY_NAME', value=partition_key_name)
        getConfigFunction.add_environment(key='SORT_KEY_NAME', value=sort_key_name)

        api = aws_apigateway.RestApi(self, id="api")

        api.root.add_method('ANY')

        path = api.root.add_resource('config')
    
        saveConfigIntegration = aws_apigateway.LambdaIntegration(saveConfigFunction)
        getConfigIntegration = aws_apigateway.LambdaIntegration(getConfigFunction)

        partition = path.add_resource('{'+partition_key_name+'}')
        partition.add_method('GET', getConfigIntegration)
        partition.add_method('POST', saveConfigIntegration)

