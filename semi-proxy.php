<?php
/**
 * Proxy PHP para /semi/ → FastAPI (puerto cPanel)
 * COLOCAR EN: /home/usuario/public_html/public/semi-proxy.php
 * 
 * Este script es más compatible en hosting compartido que mod_proxy
 */

// CONFIGURACIÓN: Cambia este puerto por el que asigne cPanel Python App
define('FASTAPI_PORT', getenv('FASTAPI_PORT') ?: '8555');
define('FASTAPI_HOST', '127.0.0.1');

// Obtener la ruta solicitada después de /semi/
$requestUri = $_SERVER['REQUEST_URI'];
$path = parse_url($requestUri, PHP_URL_PATH);

// Extraer todo lo que viene después de /semi
$basePath = '/semi';
$subPath = '';
if (strpos($path, $basePath) === 0) {
    $subPath = substr($path, strlen($basePath));
}
if ($subPath === '') $subPath = '/';

// Query string
$queryString = $_SERVER['QUERY_STRING'] ? '?' . $_SERVER['QUERY_STRING'] : '';

// Construir URL destino
$targetUrl = "http://" . FASTAPI_HOST . ":" . FASTAPI_PORT . $subPath . $queryString;

// Preparar headers a reenviar
$headers = [];
foreach ($_SERVER as $key => $value) {
    if (strpos($key, 'HTTP_') === 0) {
        $headerName = str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($key, 5)))));
        if (!in_array($headerName, ['Host', 'Connection', 'Content-Length'])) {
            $headers[] = "$headerName: $value";
        }
    }
}

// Headers adicionales importantes
$headers[] = 'Host: ' . FASTAPI_HOST . ':' . FASTAPI_PORT;
$headers[] = 'X-Forwarded-For: ' . ($_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR']);
$headers[] = 'X-Forwarded-Proto: ' . (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http');
$headers[] = 'X-Forwarded-Host: ' . $_SERVER['HTTP_HOST'];
$headers[] = 'X-Original-URI: ' . $requestUri;

// Inicializar cURL
$ch = curl_init($targetUrl);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => false, // No seguir redirects automáticamente
    CURLOPT_MAXREDIRS => 5,
    CURLOPT_TIMEOUT => 60,
    CURLOPT_CONNECTTIMEOUT => 10,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_HEADER => true, // Incluir headers en respuesta
    CURLOPT_CUSTOMREQUEST => $_SERVER['REQUEST_METHOD'],
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_SSL_VERIFYHOST => false,
]);

// Enviar body si es POST/PUT/PATCH
if (in_array($_SERVER['REQUEST_METHOD'], ['POST', 'PUT', 'PATCH', 'DELETE'])) {
    $input = file_get_contents('php://input');
    if ($input) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $input);
    }
}

// Ejecutar
$response = curl_exec($ch);
$curlError = curl_error($ch);
$curlErrno = curl_errno($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
curl_close($ch);

if ($curlErrno) {
    http_response_code(502);
    echo "Proxy Error ($curlErrno): $curlError";
    error_log("FastAPI Proxy Error: $curlErrno - $curlError - URL: $targetUrl");
    exit;
}

// Separar headers y body
$responseHeaders = substr($response, 0, $headerSize);
$responseBody = substr($response, $headerSize);

// Enviar headers de respuesta (filtrar algunos)
foreach (explode("\r\n", $responseHeaders) as $header) {
    if ($header === '') continue;
    // No reenviar headers problemáticos
    if (stripos($header, 'Transfer-Encoding:') === 0) continue;
    if (stripos($header, 'Content-Encoding:') === 0) continue;
    if (stripos($header, 'Connection:') === 0) continue;
    header($header, false, $httpCode);
}

// Establecer código de estado HTTP
http_response_code($httpCode);

// Imprimir body
echo $responseBody;