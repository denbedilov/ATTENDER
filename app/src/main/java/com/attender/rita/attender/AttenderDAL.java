package com.example.rita.attender;

import android.util.JsonReader;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;

import javax.json.Json;
import javax.json.stream.JsonParser;

/**
 * Created by Shai on 03/05/2015.
 */
public class AttenderDAL
{
    public AttenderDAL()
    {

    }

    public JSONArray getEvents(String eventType, String eventDate, String eventLocation)
    {
        FileInputStream json = null;
        JSONObject jsonObject = null;
        JSONArray jsonArray = null;

        String jsonData = "{\n" +
                "     \"Events\":\n" +
                "     [\n" +
                "         {\"id\": 1, \"name\": \"e5\", \"date\": \"1322018752992l\", \"city\": \"jerusalem1\", \"address\": \"jaffa st. 1\", \"description\": \"rbfdb bfdbfd bfdbd1\", \"event_url\": \"www.abcd1.com\" , \"host\": \"bfdbfdb1\", \"price\": \"487\"},\n" +
                "         {\"id\": 2, \"name\": \"e2\", \"date\": \"1322018452992l\", \"city\": \"jerusalem2\", \"address\": \"jaffa st. 2\", \"description\": \"rbfdb bfdbfd bfdbd2\", \"event_url\": \"www.abcd1.com\" , \"host\": \"bfdbfdb2\", \"price\": \"624\"},\n" +
                "         {\"id\": 3, \"name\": \"e3\", \"date\": \"1322028752992l\", \"city\": \"jerusalem3\", \"address\": \"jaffa st. 3\", \"description\": \"rbfdb bfdbfd bfdbd3\", \"event_url\": \"www.abcd1.com\" , \"host\": \"bfdbfdb3\", \"price\": \"872\"},\n" +
                "     ]\n" +
                " }";
        try
        {

            jsonObject = new JSONObject(jsonData);
            jsonArray = jsonObject.getJSONArray("Events");
        }
        catch (org.json.JSONException e)
        {

        }

        return jsonArray;
    }

}
