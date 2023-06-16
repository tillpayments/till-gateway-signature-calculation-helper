import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.codec.digest.DigestUtils;

public class SignatureGenerator {
    // line 1 = http request type

    // line 2
    private static String calculateHashedPayload(String payload) {
        return DigestUtils.sha512Hex(payload);
    }

    // line 3 = MIME

    // line 4
    private static String getFormattedTimeDate() {
        ZonedDateTime utcDateTime = ZonedDateTime.now(ZoneId.of("UTC"));
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("E, dd MMM yyyy HH:mm:ss z", Locale.ENGLISH);
        return utcDateTime.format(formatter);
    }

    // line 5
    private static String getRequestUri(String apiKey, String txType) {
        return "/api/v3/transaction/" + apiKey + "/" + txType;
    }

    private static String buildFiveLineStringMessage(String httpMethod, String payload, String contentType, String apiKey, String txType) {
        String codeSampleTimestamp = "Tue, 21 Jul 2020 13:15:03 UTC";

        
        return String.format("%s\n%s\n%s\n%s\n%s", httpMethod, calculateHashedPayload(payload), contentType, codeSampleTimestamp, getRequestUri(apiKey,txType));
        // return String.format("%s\n%s\n%s\n%s\n%s", httpMethod, calculateHashedPayload(payload), contentType, getFormattedTimeDate(), getRequestUri(apiKey,txType));
    }

    public static String getAuthHeader(String httpMethod, String payload, String contentType, String apiKey, String txType, String sharedSecret) {
        String msg = buildFiveLineStringMessage(httpMethod, payload, contentType, apiKey, txType);
        // System.out.println(msg);

        try {
            Mac sha512Hmac = Mac.getInstance("HmacSHA512");
            SecretKeySpec secretKey = new SecretKeySpec(sharedSecret.getBytes(), "HmacSHA512");
            sha512Hmac.init(secretKey);
            byte[] hmacBytes = sha512Hmac.doFinal(msg.getBytes());
            return Base64.encodeBase64String(hmacBytes);
        } 
        catch (NoSuchAlgorithmException | InvalidKeyException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        // obtain from application
        String httpMethod = "POST";
        String apiKey = "my-api-key";
        String sharedSecret = "my-shared-secret";
        String payload = "{\"merchantTransactionId\":\"2019-09-02-0004\",\"amount\":\"9.99\",\"currency\":\"EUR\"}";
        String contentType = "application/json; charset=utf-8";
        String txType = "debit";

        String sig = getAuthHeader(httpMethod, payload, contentType, apiKey, txType, sharedSecret);
        System.out.println(sig);
    }
}
