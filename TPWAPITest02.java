import okhttp3.*;
import java.util.Iterator;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;
import java.io.IOException;

public class TPWAPITest02 {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        try{
            OkHttpClient client = new OkHttpClient().newBuilder()
                    .build();
            MediaType mediaType = MediaType.parse("application/json");
            RequestBody body = RequestBody.create(mediaType, "{\r\n    \"login\": \"______________\",\r\n    \"password\": \"_______________\"\r\n}");
            Request request = new Request.Builder()
                    .url("________________________")
                    .method("POST", body)
                    .addHeader("Accept-Encoding", "application/json")
                    .addHeader("Accept", "application/json")
                    .addHeader("Content-Type", "application/json")
                    .build();
            Response Response1 = client.newCall(request).execute();
            System.out.println("\n\nOkHttpClient response.body().string()");
            String CocoIsland = Response1.body().string();
            System.out.println(CocoIsland);
            System.out.println("\n\nOkHttpClient response.header(\"Set-Cookie\")");
            System.out.println(Response1.header("Set-Cookie"));

            JSONObject JSONOutputString1 = new JSONObject(CocoIsland);
            String sessionToken1 = (String) JSONOutputString1.get("sessionToken");
            String thingparkID = (String) JSONOutputString1.get("thingparkID");
            String Cookies1 = Response1.header("Set-Cookie");

            

        } catch (IOException ioException) {
            ioException.printStackTrace();
        }
    }
}