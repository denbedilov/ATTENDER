package com.attender.rita.attender;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Spinner;

import com.attender.R;

import java.sql.Date;
import java.util.ArrayList;


public class searchEventActivity extends Activity
{
    AttenderBL bl;

    ArrayList<Event> events;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        bl = new AttenderBL();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_event);
        Spinner typeSpinner = (Spinner) findViewById(R.id.type_spinner);
        Spinner dateSpinner = (Spinner) findViewById(R.id.date_spinner);
        Spinner citySpinner = (Spinner) findViewById(R.id.city_spinner);

        ListView listView = (ListView) findViewById(R.id.listView);
        events = bl.getEvents("type", "fds", "fdsf");  ///!!!!!!!!!!!!!!!!!!!!!!!!!!

        EventAdapter adapter = new EventAdapter(this, events);
        listView.setAdapter(adapter);


        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            private int position;

            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Intent myIntent = new Intent(getApplicationContext(), Event_Page_Activity.class);
                this.position = position;
                int eventNum= this.position;
                myIntent.putExtra("currentEventId",events.get(eventNum).getId());
                startActivity(myIntent);
            }
        });

        ArrayAdapter<CharSequence> type_adapter = ArrayAdapter.createFromResource(this,
                R.array.type_array, android.R.layout.simple_spinner_item);
        ArrayAdapter<CharSequence> date_adapter = ArrayAdapter.createFromResource(this,
                R.array.dates_array, android.R.layout.simple_spinner_item);
        ArrayAdapter<CharSequence> city_adapter = ArrayAdapter.createFromResource(this,
                R.array.cities_array, android.R.layout.simple_spinner_item);

        type_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        date_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        city_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);


        dateSpinner.setAdapter(date_adapter);
        typeSpinner.setAdapter(type_adapter);
        citySpinner.setAdapter(city_adapter);

    }

    public void itemPressed(View v)
    {
        Intent intent=new Intent(this,Event_Page_Activity.class);
        startActivity(intent);
    }
    public void explorePressed(View v)
    {
        Intent intent=new Intent(this,CalendarPageActivity.class);
        startActivity(intent);
    }
    public void chatPressed(View v)
    {
        Intent intent=new Intent(this,ChatPageActivity.class);
        startActivity(intent);
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_search_event, menu);
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
