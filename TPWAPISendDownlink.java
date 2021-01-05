import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import java.time.ZonedDateTime;
import java.util.List;
import org.apache.commons.codec.digest.DigestUtils;
import java.time.format.DateTimeFormatter;

public class TPWAPISendDownlink {
    public static void main(String[] args) {

        String TPWAPIRootURL = "__________________";
        String DevEUI = "___________";
        String FPort = "5";
        String Payload = "__________";
        String AS_ID = "__________";
        String LRCASKey = "______________";

        ZonedDateTime dateTime = ZonedDateTime.now();
        String TimeStampSHA = dateTime.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        String TimeStampURL = TimeStampSHA.replace(":", "%3A");
        TimeStampURL = TimeStampURL.replace("+", "%2B");
        String QueryStringSHA = "DevEUI=" + DevEUI + "&FPort=" + FPort + "&Payload=" + Payload + "&AS_ID=" + AS_ID + "&Time=" + TimeStampSHA;
        String SHA2String = QueryStringSHA + LRCASKey;
        String SHA2Token = DigestUtils.sha256Hex(SHA2String);
        String QueryStringURL = "DevEUI=" + DevEUI + "&FPort=" + FPort + "&Payload=" + Payload + "&AS_ID=" + AS_ID + "&Time=" + TimeStampURL;
        String FullURL = TPWAPIRootURL + "/thingpark/lrc/rest/downlink?" + QueryStringURL + "&Token=" + SHA2Token;

        try {
            Unirest.setTimeouts(0, 0);

            HttpResponse<String> SendDownlink = Unirest.post(FullURL)
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .body("")
                    .asString();

            System.out.println("Body: " + SendDownlink.getBody());
            System.out.println("Headers: " + SendDownlink.getHeaders());
            System.out.println("Get Status: " + SendDownlink.getStatus());
            System.out.println("Get Status Text: " + SendDownlink.getStatusText());
            List<String> RequestCookies = SendDownlink.getHeaders().get("Set-Cookie");
            System.out.println("Cookies: " + RequestCookies);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}