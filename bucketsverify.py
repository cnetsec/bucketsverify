import boto3

# Criar um cliente S3
s3_client = boto3.client('s3')

# Ler a lista de buckets do arquivo de texto
with open('buckets.txt', 'r') as file:
    bucket_names = [line.strip() for line in file if line.strip()]

# Verificar as permissões de cada bucket
for bucket_name in set(bucket_names):
    try:
        # Obter as permissões do bucket
        acl_response = s3_client.get_bucket_acl(Bucket=bucket_name)

        # Exemplo de verificação se o bucket é público
        is_public = any('URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers' for grant in acl_response['Grants'])

        if is_public:
            print(f"O bucket '{bucket_name}' é Público!")
        else:
            print(f"O bucket '{bucket_name}' é Privado.")

    except Exception as e:
        if 'AllAccessDisabled' in str(e):
            print(f"O bucket '{bucket_name}' não encontrado ou desativado.")
        else:
            print(f"O bucket '{bucket_name}' ocorreu um erro: {str(e)}")
