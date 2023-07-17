using System;
using System.Security.Cryptography;
using System.Text;
using RestSharp;
using RestSharp.Authenticators;

public class SignatureGenerator
{
    // line 1 = http request type

    // line 2
    private static string CalculateHashedPayload(string payload)
    {
        using (SHA512 sha512 = SHA512.Create())
        {
            byte[] payloadBytes = Encoding.UTF8.GetBytes(payload);
            byte[] hashBytes = sha512.ComputeHash(payloadBytes);
            return BitConverter.ToString(hashBytes).Replace("-", "").ToLowerInvariant();
        }
    }

    // line 3 = MIME

    // line 4
    private static string GetFormattedTimeDate()
    {
        DateTime utcDateTime = DateTime.UtcNow;
        return utcDateTime.ToString("R");
    }

    // line 5
    private static string GetRequestUri(string apiKey, string txType)
    {
        return $"/api/v3/transaction/{apiKey}/{txType}";
    }

    private static string BuildFiveLineStringMessage(string httpMethod, string payload, string contentType, string apiKey, string txType)
    {
        string codeSampleTimestamp = "Tue, 21 Jul 2020 13:15:03 UTC";
        return string.Format("{0}\n{1}\n{2}\n{3}\n{4}", httpMethod, CalculateHashedPayload(payload), contentType, codeSampleTimestamp, GetRequestUri(apiKey, txType));
    }

    public static string GetAuthHeader(string httpMethod, string payload, string contentType, string apiKey, string txType, string sharedSecret)
    {
        string msg = BuildFiveLineStringMessage(httpMethod, payload, contentType, apiKey, txType);
        Console.WriteLine(msg);

        using (HMACSHA512 sha512Hmac = new HMACSHA512(Encoding.UTF8.GetBytes(sharedSecret)))
        {
            byte[] hmacBytes = sha512Hmac.ComputeHash(Encoding.UTF8.GetBytes(msg));
            return Convert.ToBase64String(hmacBytes);
        }
    }

    public static void Main(string[] args)
    {
        // obtain from application
        string httpMethod = "POST";
        string apiKey = "my-api-key";
        string sharedSecret = "my-shared-secret";
        string payload = "{\"merchantTransactionId\":\"2019-09-02-0004\",\"amount\":\"9.99\",\"currency\":\"EUR\"}";
        string contentType = "application/json; charset=utf-8";
        string txType = "debit";

        string sig = GetAuthHeader(httpMethod, payload, contentType, apiKey, txType, sharedSecret);
        Console.WriteLine(sig);
    }
}
