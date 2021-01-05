import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import java.util.Iterator;
import java.util.List;
import org.json.JSONArray;
import org.json.JSONObject;

public class TPWAPITest01 {
    public static void main(String[] args) {

        String TPWAPIRootURL = "_______________";
        String TPWAPIUser = "__________________";
        String TPWAPIPassword = "______________";
        String TPWSupplierID = "______";
        String TPWModuleID = "_______";

        try {
            Unirest.setTimeouts(0, 0);

            // I - Authenticate using Admin/User Credentials on ThingPark OS
            HttpResponse<String> Response1 = Unirest.post(TPWAPIRootURL + "/thingpark/smp/rest/admins/login")
                    .header("Accept-Encoding", "application/json")
                    .header("Accept", "application/json")
                    .header("Content-Type", "application/json")
                    .body("{\"login\": \"" + TPWAPIUser + "\",\"password\": \"" + TPWAPIPassword + "\"}")
                    .asString();

            JSONObject JSONOutputString1 = new JSONObject(Response1.getBody());
            String sessionToken1 = (String) JSONOutputString1.get("sessionToken");
            String thingparkID = (String) JSONOutputString1.get("thingparkID");
            List<String> Cookies1 = Response1.getHeaders().get("Set-Cookie");

            // II - Generate an Admin Access Code providing a Supplier ID and a Module ID
            HttpResponse<String> Response2 = Unirest.post(TPWAPIRootURL + "/thingpark/smp/rest/admins/"
                    + thingparkID + "/accessCode?sessionToken=" + sessionToken1)
                    .header("Accept-Encoding", "application/json")
                    .header("Accept", "application/json")
                    .header("Content-Type", "application/json")
                    .header("Cookie", String.valueOf(Cookies1))
                    .body("{\"supplierID\": \"" + TPWSupplierID + "\", \"moduleID\": \"" + TPWModuleID + "\"}")
                    .asString();
            List<String> Cookies2 = Response2.getHeaders().get("Set-Cookie");

            JSONObject JSONOutputString2 = new JSONObject(Response2.getBody());
            String accessCode = (String) JSONOutputString2.get("accessCode");

            // III - Create a session on ThingPark Wireless API
            HttpResponse<String> Response3 = Unirest.get(TPWAPIRootURL +
                    "/thingpark/wireless/rest/partners?adminAccessCode=" + accessCode + "&type=SUPPLIER")
                    .header("Accept-Encoding", "application/json")
                    .header("Accept", "application/json")
                    .header("Content-Type", "application/json")
                    .header("Cookie", String.valueOf(Cookies2))
                    .asString();
            List<String> Cookies3 = Response3.getHeaders().get("Set-Cookie");

            JSONObject JSONOutputString3 = new JSONObject(Response3.getBody());
            String sessionToken2 = (String) JSONOutputString3.get("sessionToken");
            JSONObject JSONPartner = JSONOutputString3.getJSONObject("partner");
            Object PartnerHREF = JSONPartner.get("href");

            // IV - TPWAction / Retrieve All BSS
            HttpResponse<String> Response4 = Unirest.get(TPWAPIRootURL + "/thingpark/wireless/rest" + PartnerHREF
                    + "/bss?sessionToken=" + sessionToken2)
                    .header("Accept-Encoding", "application/json")
                    .header("Accept", "application/json")
                    .header("Content-Type", "application/json")
                    .header("Cookie", String.valueOf(Cookies3))
                    .asString();
            List<String> Cookies4 = Response4.getHeaders().get("Set-Cookie");
            JSONObject JSONOutputString4 = new JSONObject(Response4.getBody());
            JSONArray JSONBriefs = JSONOutputString4.getJSONArray("briefs");

            Iterator iterator1 = JSONBriefs.iterator();
            Object key ;
            int i = 0;
            while (iterator1.hasNext()) {
                key = iterator1.next();
                JSONObject BSSEntry = new JSONObject(key.toString());
                String BSSName = (String) BSSEntry.get("name");
                String BSSLRRID = (String) BSSEntry.get("lrrID");
                String BSSHREF = (String) BSSEntry.get("href");
                System.out.print(++i);
                System.out.print("/ ");
                System.out.print(BSSName);
                System.out.print(" ");
                System.out.print(BSSLRRID);
                System.out.print(" ");
                if ((BSSEntry.get("lat") != JSONObject.NULL) && (BSSEntry.get("lon") != JSONObject.NULL)) {
                    String BSSLatitude = Double.toString((Double) BSSEntry.get("lat"));
                    String BSSLongitude = Double.toString((Double) BSSEntry.get("lon"));
                    System.out.print(" @ Latitude: ");
                    System.out.print(BSSLatitude);
                    System.out.print(" & Longitude: ");
                    System.out.print(BSSLongitude);
                }

                // V - TPWAction / Retrieve BSS Details
                HttpResponse<String> Response5 = Unirest.get(TPWAPIRootURL + BSSHREF + "?sessionToken=" + sessionToken2)
                        .header("Accept-Encoding", "application/json")
                        .header("Accept", "application/json")
                        .header("Content-Type", "application/json")
                        .header("Cookie", String.valueOf(Cookies4))
                        .asString();
                List<String> Cookies5 = Response5.getHeaders().get("Set-Cookie");
                JSONObject JSONOutputString5 = new JSONObject(Response5.getBody());
                JSONObject JSONOutputStringBSSINTS = (JSONObject) JSONOutputString5.get("ints");
                System.out.print(" ");
                JSONArray JSONOutputStringBSSINTArray = JSONOutputStringBSSINTS.getJSONArray("int");
                JSONObject ETHInterface = JSONOutputStringBSSINTArray.getJSONObject(0);
                JSONObject PPPInterface = JSONOutputStringBSSINTArray.getJSONObject(1);
                System.out.print("ETH: ");
                System.out.print(ETHInterface.get("ip"));
                System.out.print(" PPP: ");
                System.out.print(PPPInterface.get("ip"));
                System.out.println();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}