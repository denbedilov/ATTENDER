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
 * Created by Shai Pe'er on 03/05/2015.
 */
public class AttenderDAL
{
    final String API_URL = "http://attender-mobile.appspot.com/api";     //api url


    //=============================================== BUILDER ==============================================================================

    public AttenderDAL()
    {

    }


    //=============================================== GET EVENTS ==============================================================================

    public JSONArray getEvents(String eventType, String eventDate, String eventLocation)
    {
        JSONObject jsonObject = null;
        JSONArray jsonArray   = null;
        String jsonData = "";

       // Query format: ?[category=***]&[time=***]&[city=***]";
        String query = "?";
        if(eventType.compareTo("Type") != 0)             query += "category="     + eventType + "&";
        if(eventDate.compareTo("Date") != 0)             query += "time="     + eventDate + "&";
        if(eventLocation.compareTo("City") != 0)         query += "city="     + eventLocation;
        if (query.endsWith("&") || query.endsWith("?"))  query = query.substring(0, query.length() - 1); //delete the last char if it '&'


        try
        {
            jsonData = "{ Events:\n";
                //URL url = new URL("http://attender-mobile.appspot.com/api?city=Jerusalem");   //for TESTING!!!
                URL url = new URL(API_URL + query);
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                jsonData += readJsonStream(con.getInputStream());
            jsonData += "}";

            jsonObject = new JSONObject(jsonData);
            jsonArray = jsonObject.getJSONArray("Events");

        }
        catch (Exception e)
        {
            return null;
        }

        return jsonArray;
    }


    //=========================================== READ STREAM ==================================================================================

    private String readJsonStream(InputStream in)
    {
        BufferedReader reader = null;
        String jsonStreamString = "";
        try
        {
            reader = new BufferedReader(new InputStreamReader(in));
            String line = "";
            while ((line = reader.readLine()) != null)
            {
                jsonStreamString += line;
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        finally
        {
            if (reader != null)
            {
                try
                {
                    reader.close();
                }
                catch (IOException e)
                {
                    return "";
                }
            }
        }
        return jsonStreamString;
    }

    //=============================================================================================================================




}
