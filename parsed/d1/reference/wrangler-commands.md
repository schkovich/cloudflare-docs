```bash
npx wrangler whoami
npx wrangler d1 execute hey-hi-db --command "select len(json_extract("metadata", '$.section_summary')) as meta from LLamaNodes where idx='311113f2-15e7-41de-88cb-5237b805c539';"
```
