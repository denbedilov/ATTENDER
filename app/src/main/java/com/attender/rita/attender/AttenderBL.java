package com.attender.rita.attender;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.support.v7.app.ActionBarActivity;

import com.attender.rita.attender.AttenderDAL;
import com.attender.rita.attender.Event;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import javax.json.Json;
import javax.json.stream.JsonParser;

/**
 * Created by Shai on 03/05/2015.
 */
public class AttenderBL
{
    private AttenderDAL dal;

    public AttenderBL()
    {
       dal = new AttenderDAL();
    }


    //The function return the relevant events by search values;
    //Return values: null meaning that there are no relevant events, else return the events
    public ArrayList<Event> getEvents(String eventType, String eventDate, String eventLocation)
    {
        ArrayList<Event> events = new ArrayList<Event>();
        JSONArray jsonArr;
        jsonArr = dal.getEvents(eventType, eventDate, eventLocation);

        if(jsonArr == null)
        {
            return null;
        }
        Event ev;

        try
        {
           // JSONArray jEventArr = jo.getJSONArray("Events");
            for (int i = 0; i < jsonArr.length()-1; i++)
            {
                JSONObject childJSONObject = jsonArr.getJSONObject(i);
                ev = new Event(
                        childJSONObject.getString("id"),
                        childJSONObject.getString("date"),
                        childJSONObject.getString("name"),
                        childJSONObject.getString("time"),
                        childJSONObject.getString("address"),
                        childJSONObject.getString("description"),
                        childJSONObject.getString("performer")
                );
                events.add(ev);
            }

        }
        catch(JSONException e)
        {
           events = null;
        }

        return events;
    }




}
