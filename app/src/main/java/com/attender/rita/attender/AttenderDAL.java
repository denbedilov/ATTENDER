package com.attender.rita.attender;

import android.content.Context;
import android.os.AsyncTask;
import android.util.JsonReader;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.BufferedHttpEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.LinkedList;
import java.util.Scanner;

import javax.json.Json;
import javax.json.stream.JsonParser;

/**
 * Created by Shai on 03/05/2015.
 */
public class AttenderDAL
{
    final String apiUrl = "http://attender-mobile.appspot.com/api";

    static final String DEBUG_TAG = "HttpExample";
    EditText urlText;


    public AttenderDAL()
    {

    }

    public JSONArray getEvents(String eventType, String eventDate, String eventLocation)
    {
        FileInputStream json = null;
        JSONObject jsonObject = null;
        JSONArray jsonArray = null;

        String query = "?time=1m&city=Jerusalem";
/*      String query = "?";
        if(eventType != "Type")             query += "category=" + eventType;
        if(eventDate != "Date")             query += "time="     + eventDate;
        if(eventLocation != "Location")     query += "city="     + eventLocation;
*/

        //String jsonData = getJson(query);
        String jsonData = "";// = readStream(con.getInputStream());
        try {
            URL url = new URL("http://attender-mobile.appspot.com/api?city=Jerusalem");
            HttpURLConnection con = (HttpURLConnection) url
                    .openConnection();
            jsonData = readStream(con.getInputStream());
        } catch (Exception e) {
            e.printStackTrace();
        }

     //   ?city=Jerusalem
        /*
        String jsonData = "{\n" +
                "     \"Events\":\n" +
                "     [\n" +
                "         {\"id\": 1, \"name\": \"e5\", \"date\": \"1322018752992\", \"city\": \"jerusalem1\", \"address\": \"jaffa st. 1\", \"description\": \"rbfdb bfdbfd bfdbd1\", \"event_url\": \"www.abcd1.com\" , \"host\": \"bfdbfdb1\", \"price\": \"487\"},\n" +
                "         {\"id\": 2, \"name\": \"e2\", \"date\": \"1322018452992\", \"city\": \"jerusalem2\", \"address\": \"jaffa st. 2\", \"description\": \"rbfdb bfdbfd bfdbd2\", \"event_url\": \"www.abcd1.com\" , \"host\": \"bfdbfdb2\", \"price\": \"624\"},\n" +
                "         {\"id\": 3, \"name\": \"e3\", \"date\": \"1322028752992\", \"city\": \"jerusalem3\", \"address\": \"jaffa st. 3\", \"description\": \"rbfdb bfdbfd bfdbd3\", \"event_url\": \"www.abcd1.com\" , \"host\": \"bfdbfdb3\", \"price\": \"872\"},\n" +
                "     ]\n" +
                " }";
                */
        String str = "{\n" +
                "     \"Events\":\n";
        str+= jsonData + "}";
        try
        {

            jsonObject = new JSONObject(str);
            jsonArray = jsonObject.getJSONArray("Events");
        }
        catch (org.json.JSONException e)
        {
            return null;
        }

        return jsonArray;
    }

    private String readStream(InputStream in) {
        BufferedReader reader = null;
        String str = "";
        try {
            reader = new BufferedReader(new InputStreamReader(in));
            String line = "";
            while ((line = reader.readLine()) != null) {
                str += line;
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return str;
    }




}
