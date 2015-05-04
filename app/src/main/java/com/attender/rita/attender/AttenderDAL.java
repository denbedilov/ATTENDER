package com.attender.rita.attender;

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
                "         {\"id\": 1, \"name\": \"e5\", \"date\": \"01/01/01\", \"time\": \"01:00\", \"address\": \"jerusalem, jaffa st. 1\", \"description\": \"rbfdb bfdbfd bfdbd1\", \"performer\": \"bfdbfdb1\"},\n" +
                "         {\"id\": 2, \"name\": \"e2\", \"date\": \"02/02/02\", \"time\": \"02:00\", \"address\": \"jerusalem, jaffa st. 2\", \"description\": \"rbfdb bfdbfd bfdbd2\", \"performer\": \"bfdbfdb2\"},\n" +
                "         {\"id\": 3, \"name\": \"e3\", \"date\": \"03/03/03\", \"time\": \"03:00\", \"address\": \"jerusalem, jaffa st. 3\", \"description\": \"rbfdb bfdbfd bfdbd3\", \"performer\": \"bfdbfdb3\"},\n" +
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
