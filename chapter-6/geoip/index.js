
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {

	ip4_regex =/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
	ip6_regex = /^[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}\:[a-fA-F0-9]{1, 4}$/
  const path = new URL(request.url).pathname.split('/')
  const pair_pattern=/^[A-Z]+\-[A-Z]+$/
  const ipAddr=path[1]
  if( path.length !== 2 || ( ip4_regex.test(ipAddr) !== true && ip6_regex.test(ipAddr) !== true )){
    return new Response( '{"message":"ERROR: Unsupported API call"}', {
      headers: { 'content-type': 'text/json' },
      status: 400,
      satusText: 'Bad request',
      })
  }

  const APIKey = request.headers.get('X-API-Key')
  if( APIKey === null  ) {
  return new Response( '{"message":"ERROR: Unauthorized request 1"}', {
    headers: { 'content-type': 'text/json' },
    status: 403,
    satusText: 'Unauthorized Request',
    })
  }

  const validAPI =  await geo_apikeys.get( APIKey )
  if( validAPI == null ){
  return new Response( '{"message":"ERROR: Unauthorized request 2"}', {
    headers: { 'content-type': 'text/json' },
    status: 403,
    satusText: 'Unauthorized Request',
    })
  }

  const maxmind_url="https://geolite.info/geoip/v2.1/city/" + ipAddr + "?pretty"
  const result = await fetch(maxmind_url, {
    headers: new Headers({
    "authorization": "Basic " + btoa(unescape(encodeURIComponent(MAXMIND_API_ACCOUNT+":"+MAXMIND_API_KEY)))
    })
  })
  geoData = await result.json()
  const minGeoData = { country: geoData['country']['iso_code'],
	  latitude: geoData['location']['latitude'],
	  longitude: geoData['location']['longitude'],
  }
  return new Response(JSON.stringify(minGeoData), {
    headers: { 'content-type': 'text/json' },
  })

}




