package com.attender.rita.attender;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import com.attender.R;

import java.sql.Date;
import java.util.ArrayList;

public class ChatPageActivity extends Activity
{
    AttenderBL bl;
    ArrayList<Event> events;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        bl = new AttenderBL();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat_page);
        ListView listView = (ListView) findViewById(R.id.listView);

        events = bl.getEvents("type", "fds", "fdsf");  ///!!!!!!!!!!!!!!!!!!!!!!!!!!

        EventAdapter adapter = new EventAdapter(this, events);
        listView.setAdapter(adapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            // private int position;

            public void onItemClick(AdapterView<?> parent, View view, int position, long id)
            {
                Intent myIntent = new Intent(getApplicationContext(), Event_Page_Activity.class);
                int eventNum = position;
                Event testE = events.get(eventNum);
                myIntent.putExtra("CurrentEvent",events.get(eventNum));
                startActivity(myIntent);
            }
        });
    }
    public void eventsPressed(View v)
    {
        Intent intent=new Intent(this,searchEventActivity.class);
        startActivity(intent);
    }
    public void explorePressed(View v)
    {
        Intent intent=new Intent(this,CalendarPageActivity.class);
        startActivity(intent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_chat_page, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
