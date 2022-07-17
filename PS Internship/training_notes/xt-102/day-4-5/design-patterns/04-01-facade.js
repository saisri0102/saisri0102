// What is "facade"
// Facade tries to simply APIs and provide a more convenient interface
// Helps making changes easy
function makeAjaxRequest( { method, endpoint, body, authenticated } ) {
    const headers = new Headers();
    
    const requestOptions = {
        method: method,
        headers: headers,
        redirect: 'follow'
    };

    if( body ) {
        headers.append( 'Content-Type', 'application/json' );
        requestOptions.body = JSON.stringify( body );
    }

    if( authenticated ) {
        headers.append( 'Authorization', 'Bearer ' + getToken() );
    }

    // sanity check: remove leading slash (if any)
    if( endpoint.substr( 0, 1 ) === '/' ) {
        endpoint = endpoint.substr( 1 );
    }

    return fetch( `${AppConfig.API_BASE_URL}/${endpoint}`, requestOptions )
        .then(async function( response ) {
            if( !response.ok ) {
                const error = await response.json();
                
                const customError = new Error( 'Something went wrong with the request' );
                customError.errorResponse = error;
                
                throw customError;
            }
            
            return response.json();
        });
}

return makeAjaxRequest({
    method: 'GET',
    endpoint: 'workshops',
    authenticated: true
});