# Requirement Knowledge Card

<!-- sc:manifest -->
```json
{"schema_version":"supercoder.trace/v1","repository_id":"demo-repo","development_project_id":"demo-20260715","resource":{"id":"req-1","type":"Requirement","revision":1,"digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","status":"DISCOVERED","owner":"analysis","ref":"sc://demo-repo/demo-20260715/requirement/req-1"},"entities":[{"id":"module-1","type":"Module","revision":1,"digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","status":"CANDIDATE","owner":"product-module-registry","ref":"sc://demo-repo/demo-20260715/module/module-1"},{"id":"evidence-1","type":"Evidence","revision":1,"digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","status":"ACTIVE","owner":"review","ref":"sc://demo-repo/demo-20260715/evidence/evidence-1"}],"relations":[{"id":"rel-1","type":"REQUIREMENT_ALLOCATED_TO_MODULE","source_ref":"sc://demo-repo/demo-20260715/requirement/req-1","target_ref":"sc://demo-repo/demo-20260715/module/module-1","state":"ACTIVE"}],"sections":[{"id":"changes","digest":"80febce6b7784f0a0bc46cb32564e1bd144202a573dca50442a7b55fd4ae9a29"},{"id":"risks","digest":"5202f4336d7a51e7df5618e8f62a0735d7867409e1358bf378bd99a884a8a3a0"},{"id":"relationships","digest":"49221bb6167bc92c64bead846353a2ef19f228fe0aa4266305f9acaeb3c79e6c"},{"id":"evidence","digest":"172bad3b2d98daba912006d706907a2d2365c6acefa2672f2818c25e71cec311"}],"source_digests":[]}
```
<!-- /sc:manifest -->

<!-- sc:section id="changes" digest="80febce6b7784f0a0bc46cb32564e1bd144202a573dca50442a7b55fd4ae9a29" -->
Expected and actual changes.
<!-- /sc:section -->

<!-- sc:section id="risks" digest="5202f4336d7a51e7df5618e8f62a0735d7867409e1358bf378bd99a884a8a3a0" -->
Risk risk-1 is OPEN.
<!-- /sc:section -->

<!-- sc:section id="relationships" digest="49221bb6167bc92c64bead846353a2ef19f228fe0aa4266305f9acaeb3c79e6c" -->
Requirement allocated to module-1.
<!-- /sc:section -->

<!-- sc:section id="evidence" digest="172bad3b2d98daba912006d706907a2d2365c6acefa2672f2818c25e71cec311" -->
Validation evidence: test-report-1.
<!-- /sc:section -->
