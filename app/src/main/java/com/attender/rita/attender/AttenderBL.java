package com.attender.rita.attender;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.support.v7.app.ActionBarActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

import javax.json.Json;
import javax.json.stream.JsonParser;

/**
 * Created by Shai Pe'er on 03/05/2015.
 */
public class AttenderBL
{
    private AttenderDAL dal;

    //=============================================== BUILDER ==============================================================================

    public AttenderBL()
    {
       dal = new AttenderDAL();
    }


    //=============================================== GET EVENTS ==============================================================================

    //The function return the relevant events by search values.
    //Return values: null meaning that there are no relevant events, else return the events
    public ArrayList<Event> getEvents(String eventType, String eventDate, String eventLocation)
    {
        Date date;
        Event ev;
        JSONArray jsonArr;
        ArrayList<Event> events = new ArrayList<Event>();
        DateFormat dateFormatDate = new SimpleDateFormat("dd/MM/yyyy");
        DateFormat dateFormatTime = new SimpleDateFormat("HH:mm");

        jsonArr = dal.getEvents(eventType, eventDate, eventLocation);
        if(jsonArr == null)
            return null;

        try
        {
           // JSONArray jEventArr = jo.getJSONArray("Events");
            for (int i = 0; i < jsonArr.length() - 1; i++)
            {
                JSONObject childJSONObject = jsonArr.getJSONObject(i);
                date = convertMilliSecondsToDate(childJSONObject.getString("date"));

                if(date != null)
                {
                    ev = new Event(
                            childJSONObject.getString("id"),
                            dateFormatDate.format(date),
                            childJSONObject.getString("name"),
                            dateFormatTime.format(date),
                            childJSONObject.getString("city"),
                            childJSONObject.getString("address"),
                            childJSONObject.getString("description"),
                            childJSONObject.getString("event_url"),
                            childJSONObject.getString("host"),
                            childJSONObject.getString("price"),
                            date
                    );

                    events.add(ev);
                }
            }
        }
        catch(JSONException e)
        {
           events = null;
        }

        return events;
    }

    //=============================================== CONVERT MILI-SEC TO DATE ==============================================================================

    //Convert the mili-sec string to date object, in case of fail, return null
    private Date convertMilliSecondsToDate(String miliSecDateString)
    {
        Date date = new Date();

        //int parsMili = Integer.parseInt(childJSONObject.getString("date").trim(), 16 );
        //date = convertMilliSecondsToDate("1431264600000");

        try
        {
            long milliSeconds = Long.parseLong(miliSecDateString);
            date.setTime(milliSeconds);
        }
        catch(NumberFormatException e)
        {
             return null;
        }
        return date;
    }


    //=============================================================================================================================


}
