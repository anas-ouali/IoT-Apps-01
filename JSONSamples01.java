import org.json.JSONArray;
import org.json.JSONObject;
import java.util.Iterator;

class JSONSamples01 {

    public static void main(String[] args) {
        //String JSON = "{\"LanguageLevels\":{\"1\":\"Level 1\",\"2\":\"Level 2\",\"3\":\"Level 3\",\"4\":\"Level 4\"}}\n";
        String JSON = "{\"int\":[{\"devRoundTrip\":null,\"activity\":0,\"tx\":{\"avgBitRate\":0,\"totalTraffic\":0},\"rx\":{\"avgBitRate\":0,\"totalTraffic\":0},\"signalStrength\":null,\"ip\":null,\"name\":\"eth0\",\"stateSince\":1591415187795,\"avgRoundTrip\":null,\"state\":5,\"type\":\"ETHERNET\"},{\"devRoundTrip\":16,\"activity\":5203471,\"tx\":{\"avgBitRate\":337,\"totalTraffic\":251681.69899999953},\"rx\":{\"avgBitRate\":270,\"totalTraffic\":186796.1900000013},\"signalStrength\":null,\"ip\":\"10.128.0.19\",\"name\":\"ppp0\",\"stateSince\":1594812572260,\"avgRoundTrip\":110,\"state\":0,\"type\":\"GPRS\"}]}\n";
/*
        JSONObject jsonObject = new JSONObject(JSON);
        JSONObject getSth = jsonObject.getJSONObject("int");
        Object level = getSth.get("devRoundTrip");
        System.out.println(JSON);
        System.out.println(level);
*/
        JSONObject obj1 = new JSONObject(JSON);
        JSONArray arrayObject = obj1.getJSONArray("int");
        JSONObject obj2 = new JSONObject(arrayObject);
        System.out.println(arrayObject);
        System.out.print("Coco!");
    }
}